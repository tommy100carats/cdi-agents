# -*- coding: utf-8 -*-
"""Expérience demandée par une annonce, et sa lecture pour le profil de Tom.

Règle R17 (16/09/2026, après les refus de Kolecto, Walter Learning, Believe, Dust, Pennylane) : Tom a 2 à 3 ans
en opérations (7 ans au total). Cible = postes demandant 3 ans ou moins (« coeur ») ; 4 ans = « stretch », signalé ;
5 ans et plus = « hors », écarté au sourcing. Un « Senior », « Lead », « Head » sans durée écrite = hors.
Aucune donnée → inconnu, accepté et signalé (un vide n'est pas un zéro).
"""
import re

_NUM = r"(\d{1,2})"
_UNIT = r"(?:ans|années|année|annees|years|yrs|year|an(?![a-zà-ÿ]))"
_PATTERNS = [
    # 3-5 ans / 3 à 5 ans / 3 to 5 years / 8/10 ans / 5-7 années (17/09/2026)
    re.compile(rf"{_NUM}\s*(?:-|–|à|a|to|/)\s*{_NUM}\s*\+?\s*{_UNIT}", re.IGNORECASE),
    # 3+ ans / 3 ans minimum / minimum 3 ans / at least 3 years / 3 years of experience
    re.compile(rf"(?:minimum|min\.?|at least|au moins|plus de|more than|over)?\s*{_NUM}\s*\+?\s*{_UNIT}", re.IGNORECASE),
]

# Nombres écrits en lettres (incident du 17/09/2026, NHCO : « cinq ans d'expérience » non lu).
_WORDNUM = {"un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6, "sept": 7, "huit": 8,
            "neuf": 9, "dix": 10, "douze": 12, "quinze": 15, "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "twelve": 12, "fifteen": 15}
_WORDNUM_RE = re.compile(r"(?<![a-zà-ÿ])(" + "|".join(sorted(_WORDNUM, key=len, reverse=True)) + r")(?=\s*(?:\(\d+\)\s*)?\+?\s*" + _UNIT + r"\b)", re.IGNORECASE)


def _digits(text):
    t = _WORDNUM_RE.sub(lambda m: str(_WORDNUM[m.group(1).lower()]), text or "")
    # « cinq (5) ans » -> « 5 ans »
    return re.sub(r"(\d{1,2})\s*\(\1\)", r"\1", t)
# Mots de niveau, lus dans le TITRE seulement (jamais dans le corps : « leadership », « senior team »
# y apparaissent sans rien dire du poste). Incident du 07/09/2026 : un « Junior Sales Operations Analyst »
# était classé « hors » parce que le corps contenait « lead ». Ordre : les mots juniors gagnent.
_WORDS = [("junior", 1), ("débutant", 0), ("entry level", 0), ("entry-level", 0), ("graduate", 0),
          ("associate", 1), ("head of", 8), ("director", 8), ("directeur", 8), ("directrice", 8), ("vp", 10),
          ("senior", 5), ("confirmé", 4), ("confirmée", 4), ("lead", 6)]


# Une durée ne compte que si elle parle d'expérience. Incident du 07/09/2026 : « vos données peuvent être
# conservées 2 ans » (politique RGPD en pied d'annonce) et « en 6 ans d'existence » étaient lus comme des
# années d'expérience demandées.
# Incident du 10/09/2026 : « Your data is kept for up to 2 years » (Qonto) lu comme 2 ans d'expérience.
_EXP_CONTEXT = re.compile(r"exp[ée]rience|experience|années? d'|years? (?:of|in)|yrs|minimum|at least|au moins|\+", re.IGNORECASE)
# Incident du 17/09/2026 (Qonto) : « She spent 15+ years at... » décrit une personne, pas le poste.
_PERSON = re.compile(r"\b(?:she|he|they|our (?:ceo|founder|team)|il|elle|nos fondateurs)\b[^.]{0,40}$|spent|a passé|ont passé|has (?:over|more than)|compte plus de|cumul", re.IGNORECASE)
_SOFT = re.compile(r"is a plus|a plus|nice to have|bonus|idéalement|ideally|serait un plus|appréci", re.IGNORECASE)
_NOT_EXP = re.compile(r"conserv|retain|retention|kept|keep (?:your|them)|stored|stock[ée]|gard[ée]es?|up to|jusqu'à|existence|fond[ée]e|founded|il y a|ago|depuis|since|garantie|warranty|contrat de|cdd de|mission de|tous les|every|per year|par an\b", re.IGNORECASE)


def _negated(text, start, end):
    near = text[max(0, start - 20): end + 30]
    if _NOT_EXP.search(near):
        return True
    before = re.split(r"[.!?;\n]", text[max(0, start - 60): start])[-1]  # même phrase seulement
    return bool(_PERSON.search(before))


def _in_experience_context(text, start, end):
    window = text[max(0, start - 70): end + 40]
    return bool(_EXP_CONTEXT.search(window)) and not _negated(text, start, end)


def years_required(text: str):
    """Retourne (min, max) d'années demandées, ou (None, None) si rien n'est écrit."""
    t = _digits(text)
    for m in _PATTERNS[0].finditer(t):
        # une fourchette « 3 à 5 ans » parle presque toujours d'expérience ; on n'exclut que les faux amis
        lo, hi = int(m.group(1)), int(m.group(2))
        if lo > 20 or hi > 20:
            continue
        if not _negated(t, m.start(), m.end()):
            return (min(lo, hi), max(lo, hi))
    candidates = []
    for m in _PATTERNS[1].finditer(t):
        n = int(m.group(1))
        if 0 <= n <= 20 and _in_experience_context(t, m.start(), m.end()):
            soft = bool(_SOFT.search(re.split(r"[.!?;\n]", t[m.end(): m.end() + 60])[0]))
            plus = "+" in t[m.start():m.end()] or bool(re.search(r"minimum|at least|au moins|plus de|more than|over", t[max(0, m.start() - 15):m.end()], re.I))
            candidates.append((n, plus, soft))
    if candidates:
        # 17/09/2026 : plusieurs exigences fermes (« minimum 2 ans de management » et « 5 ans d'expérience ») :
        # on garde la plus grande, c'est elle qui fait refuser un CV. Une durée « appréciée / a plus » ne compte
        # que s'il n'y a rien d'autre.
        hard = [c for c in candidates if not c[2]] or candidates
        lo, plus, _ = max(hard)
        return (lo, None if plus else lo)
    return (None, None)


def title_level(title: str):
    """Niveau implicite d'un TITRE (mot entier), ou None. Jamais appliqué au corps de l'annonce."""
    tl = (title or "").lower()
    for w, y in _WORDS:
        if re.search(r"(?<![a-zà-ÿ])" + re.escape(w) + r"(?![a-zà-ÿ])", tl):
            return y, w
    return None


def band(text: str, title: str = "") -> dict:
    """Classe l'annonce : coeur (≤ 3 ans), stretch (4 ans), hors (5 ans et plus), inconnu (R17).

    Les années écrites dans le texte priment ; à défaut, un mot de niveau dans le titre ; sinon inconnu.
    """
    lo, hi = years_required(text)
    reason = None
    if lo is None and title:
        tv = title_level(title)
        if tv:
            lo, reason = tv[0], f"aucune durée écrite ; « {tv[1]} » dans le titre"
    if lo is None:
        return {"years_min": None, "years_max": None, "band": "inconnu", "reason": "aucune durée écrite"}
    if lo <= 3:
        b = "coeur"
    elif lo <= 4:
        b = "stretch"
    else:
        b = "hors"
    return {"years_min": lo, "years_max": hi, "band": b, "reason": reason or f"{lo} an(s) minimum écrit(s)"}


def sourcing_decision(text: str, title: str = "") -> dict:
    """Décision de sourcing déterministe. « hors » est écarté avec motif ; le reste passe à Hugo."""
    b = band(text, title)
    b["keep"] = b["band"] in ("coeur", "stretch", "inconnu")
    return b
