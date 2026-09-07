#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cv_check.py : linter déterministe d'un fichier cv_data_*.py AVANT rendu et envoi.

Usage :
    python3 cv_check.py cv_data_<cible>.py            # contrôles sur les données
    python3 cv_check.py cv_data_<cible>.py --build    # + rendu PDF et contrôles de mise en page

Sortie : une ligne par contrôle (OK / FAIL / WARN), code retour 1 si au moins un FAIL.
Le générateur (cv_build.py) ne change jamais ; ce fichier encode les règles de
claude/regles-redaction-cv.md et de claude/niveau-technique-reel.md pour qu'elles soient
vérifiées par du code, pas par relecture.

Principe : tout ce qu'une règle peut trancher ne va pas au modèle, et ne va pas non plus
à la relecture humaine. Le modèle propose le contenu, le linter refuse ce qui viole une règle,
l'humain valide ce qui reste.
"""
import importlib.util
import os
import re
import subprocess
import sys

# ----------------------------------------------------------------------------- règles

# Chaînes interdites partout (règle « Tom ne code pas », « depuis zéro », chiffres périmés)
FORBIDDEN_ANYWHERE = [
    (r"\bPython\b", "langage de programmation interdit sur le CV (Tom ne code pas)"),
    (r"\bJavaScript\b", "langage de programmation interdit sur le CV"),
    (r"\bTypeScript\b", "langage de programmation interdit sur le CV"),
    (r"\bLangChain\b|\bLangGraph\b", "framework de code jamais utilisé"),
    (r"depuis z[ée]ro", "calque de l'anglais : écrire « à partir de rien »"),
    (r"\b131\b", "chiffre périmé (131 fiches) : utiliser 199 fiches en 44 jours"),
    (r"\{\{", "placeholder non rempli"),
    (r"built on n8n|tournent sur n8n|running on n8n", "les agents personnels ne tournent PAS sur n8n"),
    (r"validation humaine avant toute [ée]criture|human validation before any write",
     "affirmation fausse depuis l'audit du 06/09 : les agents 1 et 2 écrivent sans validation ; "
     "écrire « validation humaine avant toute action irréversible »"),
    (r"I like documenting|j'aime documenter", "trait de caractère non vérifié (corrigé par Tom le 10/08)"),
]

# Tirets longs : interdits dans les données (le séparateur poste/boîte est dans cv_build.py)
EM_DASH = "—"

# Outils qui exigent un qualificatif
QUALIFIED_TOOLS = [
    (r"Salesforce(?!\s*\((notions|basics|notions de base)\))", "Salesforce doit porter « (notions) »"),
    (r"HubSpot(?!\s*\((certifi[ée]|certified)\))", "HubSpot doit porter « (certifié) » dans la ligne Outils"),
]

# Chiffres autorisés (whitelist) : toute valeur M€/k€/% doit y figurer
ALLOWED_FIGURES = {
    "3 M€", "€3M", "360 k€", "€360K", "180 k€", "€180K", "350 k€", "€350K",
    "20 M€", "€20M", "+15 %", "120 %", "40 %", "25 %", "40 leads", "1 000 €", "25 €",
}
FIGURE_RE = re.compile(r"(€\s?\d[\d,\.]*\s?[MK]|\d[\d\s,\.]*\s?[Mk]€|\+?\d{1,3}\s?%)")

# Mots de langues interdits dans le Profil (déjà dans la colonne de gauche)
LANG_WORDS = [r"\banglais\b", r"\bespagnol\b", r"\bTOEIC\b", r"\bEnglish\b", r"\bSpanish\b", r"\bfluent\b"]

WITNESS_FR = "Centres d'intérêt"
WITNESS_EN = "Interests"


# ----------------------------------------------------------------------------- utilitaires

def load_data(path):
    spec = importlib.util.spec_from_file_location("cfg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.DATA


def walk(obj, trail=""):
    """Rend chaque chaîne du DATA avec son chemin (pour localiser une erreur)."""
    if isinstance(obj, str):
        yield trail, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{trail}.{k}" if trail else k)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from walk(v, f"{trail}[{i}]")


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&")


class Report:
    def __init__(self):
        self.rows = []
        self.fails = 0

    def ok(self, name, detail=""):
        self.rows.append(("OK  ", name, detail))

    def warn(self, name, detail=""):
        self.rows.append(("WARN", name, detail))

    def fail(self, name, detail=""):
        self.fails += 1
        self.rows.append(("FAIL", name, detail))

    def dump(self):
        for status, name, detail in self.rows:
            print(f"[{status}] {name}" + (f" : {detail}" if detail else ""))
        print()
        print(f"{self.fails} FAIL, {sum(1 for r in self.rows if r[0] == 'WARN')} WARN, "
              f"{sum(1 for r in self.rows if r[0] == 'OK  ')} OK")


# ----------------------------------------------------------------------------- contrôles

def check_data(d, cible, rep):
    strings = list(walk(d))
    lang = "EN" if d.get("t_profil", "Profil").lower().startswith("profile") else "FR"
    profil = strip_html(d.get("profil", ""))

    # 1. Tirets longs
    hits = [t for t, s in strings if EM_DASH in s]
    if hits:
        rep.fail("Aucun tiret long", f"{len(hits)} chaîne(s) : {', '.join(hits[:5])}")
    else:
        rep.ok("Aucun tiret long")

    # 2. Chaînes interdites
    any_forbidden = False
    for pattern, why in FORBIDDEN_ANYWHERE:
        hits = [t for t, s in strings if re.search(pattern, s, re.IGNORECASE)]
        if hits:
            any_forbidden = True
            rep.fail(f"Interdit : /{pattern}/", f"{why} ; dans {', '.join(hits[:4])}")
    if lang == "FR":
        hits = [t for t, s in strings if re.search(r"zero to one", s, re.IGNORECASE)]
        if hits:
            any_forbidden = True
            rep.fail("Interdit : « zero to one » dans un CV français",
                     "écrire « passage à l'échelle : structurer sans freiner la croissance »")
    if not any_forbidden:
        rep.ok("Chaînes interdites", "aucune")

    # 3. Outils qualifiés
    tools_lines = [s for t, s in strings if t.startswith("sidebar") and re.search(r"Salesforce|HubSpot", s)
                   and not re.search(r"Revenue Operations|Sales Management|Sales Hub", s)]  # pas les certifs
    any_bad = False
    for pattern, why in QUALIFIED_TOOLS:
        bad = [s for s in tools_lines if re.search(pattern, strip_html(s))]
        if bad:
            any_bad = True
            rep.fail("Outil qualifié", f"{why} ; ligne : {strip_html(bad[0])[:80]}")
    if not any_bad:
        rep.ok("Outils qualifiés (Salesforce, HubSpot)")

    # 4. SQL affiché en Outils (invite un test live) : avertissement, pas interdiction
    if any(t.startswith("sidebar") and re.search(r"\bSQL\b", strip_html(s)) and "Kaggle" not in s
           for t, s in strings):
        rep.warn("SQL dans les outils", "affiche SQL hors certification : invite un test live en entretien")

    # 5. emlyon en minuscules
    if re.search(r"EmLyon|EM Lyon|EMLYON|Emlyon", " ".join(s for _, s in strings)):
        rep.fail("emlyon en minuscules", "écrire « emlyon business school »")
    elif "emlyon business school" in profil:
        rep.ok("emlyon business school dans le profil")
    else:
        rep.fail("emlyon business school dans le profil", "absent de l'accroche")

    # 6. Entreprise cible nommée dans le profil
    if cible and cible.lower() in profil.lower():
        rep.ok("Entreprise cible dans le profil", cible)
    else:
        rep.fail("Entreprise cible dans le profil", f"« {cible} » introuvable (champ oublié en dupliquant ?)")

    # 7. Disponible immédiatement
    if re.search(r"Disponible imm[ée]diatement|Available immediately", profil):
        rep.ok("« Disponible immédiatement » présent")
    else:
        rep.fail("« Disponible immédiatement » présent", "absent du profil")

    # 8. Pas de langues dans le profil
    lw = [w for w in LANG_WORDS if re.search(w, profil, re.IGNORECASE)]
    if lw:
        rep.fail("Pas de langues dans le profil", f"trouvé {lw}")
    else:
        rep.ok("Pas de langues dans le profil")

    # 9. Longueur de l'accroche : 4 à 6 lignes ≈ 550 à 1 000 caractères
    n = len(profil)
    if 500 <= n <= 1050:
        rep.ok("Longueur du profil", f"{n} caractères")
    else:
        rep.warn("Longueur du profil", f"{n} caractères (cible 550 à 1 000)")

    # 10. Chiffres : tout M€/k€/% doit être dans la whitelist
    text_all = strip_html(" ".join(s for _, s in strings))
    found = set(m.strip() for m in FIGURE_RE.findall(text_all))
    unknown = sorted(f for f in found if f not in ALLOWED_FIGURES and not re.match(r"^\d{1,3}\s?%$", f) or
                     (re.match(r"^\d{1,3}\s?%$", f) and f not in ALLOWED_FIGURES))
    if unknown:
        rep.fail("Chiffres hors whitelist", f"{unknown} : vérifier la source, ou ajouter à ALLOWED_FIGURES")
    else:
        rep.ok("Chiffres dans la whitelist", ", ".join(sorted(found)) or "aucun")

    # 11. Chronologie inverse des expériences
    years = []
    for x in d.get("experiences", []):
        m = re.findall(r"(20\d{2})", x.get("dates", ""))
        years.append(int(m[-1]) if m else 0)
    if years == sorted(years, reverse=True):
        rep.ok("Chronologie inverse", " > ".join(map(str, years)))
    else:
        rep.fail("Chronologie inverse", f"ordre des années de fin : {years}")

    # 12. Agents jamais dans une puce salariée
    for x in d.get("experiences", []):
        for p in x.get("puces", []):
            if re.search(r"agents? IA|AI agents?", p, re.IGNORECASE) and "MCP" in p:
                rep.fail("Agents hors expérience salariée", f"puce de {x.get('boite')} mentionne les agents personnels")

    # 13. Photo
    photo = d.get("photo")
    if photo and os.path.exists(photo):
        rep.ok("Photo présente", photo)
    else:
        rep.fail("Photo présente", f"{photo} introuvable (recette : claude/photo-cv.md)")

    # 14. Nom de fichier de sortie : espaces, pas d'underscore
    out = d.get("out", "")
    if "_" in out:
        rep.fail("Nom du PDF sans underscore", out)
    else:
        rep.ok("Nom du PDF", out)

    return lang


def check_pdf(d, lang, rep, build_script=None):
    build_script = build_script or os.path.join(os.path.dirname(os.path.abspath(__file__)), "cv_build.py")
    out = d.get("out", "CV.pdf")
    if not os.path.exists(build_script):
        rep.warn("Rendu PDF", f"{build_script} absent, contrôles de mise en page sautés")
        return
    r = subprocess.run([sys.executable, build_script, sys.argv[1]], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        rep.fail("Rendu PDF", r.stderr.strip()[-300:])
        return
    info = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout
    pages = re.search(r"Pages:\s+(\d+)", info)
    pages = int(pages.group(1)) if pages else 0
    if pages == 1:
        rep.ok("Une page", out)
    else:
        rep.fail("Une page", f"{pages} pages")
    text = subprocess.run(["pdftotext", "-layout", out, "-"], capture_output=True, text=True).stdout
    witness = WITNESS_EN if lang == "EN" else WITNESS_FR
    if witness.lower() in text.lower():
        rep.ok("Colonne gauche complète", f"bloc témoin « {witness} » visible")
    else:
        rep.fail("Colonne gauche complète", f"bloc témoin « {witness} » absent : la sidebar déborde")


# ----------------------------------------------------------------------------- main

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    data = load_data(sys.argv[1])
    # La cible est déduite du nom de fichier : cv_data_<cible>_<lang>.py, ou passée en --cible=
    cible = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--cible=")), None)
    if not cible:
        stem = os.path.basename(sys.argv[1]).replace("cv_data_", "").replace(".py", "")
        cible = re.sub(r"_(fr|en)$", "", stem).split("_")[0]
    rep = Report()
    lang = check_data(data, cible, rep)
    if "--build" in sys.argv:
        check_pdf(data, lang, rep)
    rep.dump()
    sys.exit(1 if rep.fails else 0)
