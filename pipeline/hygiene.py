# -*- coding: utf-8 -*-
"""Hygiène du CRM : les contrôles qu'un RevOps ferait sur un pipeline, exécutés par du code.

Entrée : export JSON du CRM (requête SQL Notion, voir prompts/_protocole_commun.md).
Sortie : rapport {resume, problemes[]} avec, pour chaque problème, la gravité, la ligne et la
correction proposée. Le code ne corrige rien lui-même : Scribe applique les corrections
autorisées, Noé liste le reste pour Tom.
"""
from collections import Counter
from datetime import date, datetime

from .dedup import find_duplicates
from .keys import key_from_opportunite
from .precedence import ALL_STATUSES, ORDER, PARKED, TERMINAL

OPEN = {"Candidature envoyée", "Entretien", "Test / Étude de cas", "Offre reçue"}
UNVERIFIABLE = ("linkedin.com", "welcometothejungle.com")


def _d(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(str(s)[:10])
        except ValueError:
            return None


def norm_row(r):
    """Accepte les deux formes d'export (alias SQL ou noms Notion) et rend un dict stable."""
    g = lambda *names: next((r[n] for n in names if n in r and r[n] is not None), None)
    return {
        "url": r.get("url"),
        "opportunite": g("Opportunité") or "",
        "poste": g("Poste") or "",
        "statut": g("Statut"),
        "score": g("Score /20"),
        "role": g("Rôle cible"),
        "source": g("Source"),
        "lien": g("Lien offre"),
        "date_pub": _d(g("date_pub", "date:Date publication:start")),
        "date_cand": _d(g("date_cand", "date:Date candidature:start")),
        "relance": _d(g("relance", "date:Prochaine relance:start")),
        "cree": _d(g("cree", "Créé le", "createdTime")),
        "cle": g("Clé") or key_from_opportunite(g("Opportunité") or ""),
        "ecrit_par": g("Écrit par"),
        "notes": g("notes160", "Notes") or "",
        "doublon_tag": str(g("Opportunité") or "").startswith("🗑️"),
    }


def run(crm_rows, today=None, inbox_rows=None, runs_rows=None):
    today = today or date.today()
    rows = [norm_row(r) for r in crm_rows]
    problems = []

    def add(gravite, code, row, message, correction):
        problems.append({"gravite": gravite, "code": code, "url": row.get("url") if row else None,
                         "ligne": row.get("opportunite") if row else None, "message": message,
                         "correction": correction})

    # 1. statuts hors liste
    for r in rows:
        if r["statut"] not in ALL_STATUSES:
            add("bloquant", "statut_invalide", r, f"statut « {r['statut']} »", "choisir une option de la liste")

    # 2. doublons sur clé métier
    for k, grp in find_duplicates(crm_rows).items():
        keep = sorted(grp, key=lambda x: (x.get("cree") or x.get("Créé le") or ""))[0]
        for r in grp:
            if r is keep:
                continue
            add("majeur", "doublon_cle", norm_row(r), f"clé « {k} » en {len(grp)} exemplaires",
                f"préfixer « 🗑️ DOUBLON — », statut En veille, note vers {keep.get('url')}")

    # 3. score manquant ou hors bornes sur une fiche non close
    for r in rows:
        if r["doublon_tag"] or r["statut"] == TERMINAL:
            continue
        if r["score"] is None:
            add("majeur", "score_manquant", r, "Score /20 vide", "faire noter par Hugo_Notation")
        elif not (0 <= float(r["score"]) <= 20):
            add("bloquant", "score_hors_bornes", r, f"score {r['score']}", "renoter")

    # 4. dossiers ouverts sans date de candidature
    for r in rows:
        if r["statut"] in OPEN and not r["date_cand"]:
            add("mineur", "date_candidature_absente", r, "dossier ouvert sans date de candidature",
                "renseigner la date à partir de l'accusé de réception Gmail")

    # 5. relances : dues, absentes sur dossier ouvert
    for r in rows:
        if r["statut"] in OPEN and not r["doublon_tag"]:
            if r["relance"] and r["relance"] <= today:
                add("action", "relance_due", r, f"relance prévue le {r['relance']}", "relancer ou requalifier")
            elif not r["relance"]:
                add("mineur", "relance_absente", r, "dossier ouvert sans prochaine relance",
                    "poser J+10 après candidature, J+2 après entretien")

    # 6. « À contacter » périmées (> 14 jours sans action) et liens non vérifiables
    for r in rows:
        if r["statut"] == "À contacter" and not r["doublon_tag"]:
            age = (today - r["cree"]).days if r["cree"] else None
            if age is not None and age > 14:
                add("mineur", "a_contacter_perime", r, f"« À contacter » depuis {age} jours",
                    "décider : candidater, mettre en veille (motif daté) ou clore")
            if not r["lien"]:
                add("majeur", "lien_absent", r, "aucun lien d'offre", "retrouver le lien direct ou mettre en veille")
            elif any(h in r["lien"] for h in UNVERIFIABLE):
                add("mineur", "lien_non_verifiable", r, "lien LinkedIn / WTTJ, non vérifiable par du code",
                    "chercher le lien ATS ou carrière")

    # 7. lignes taguées doublon mais toujours dans un statut actif
    for r in rows:
        if r["doublon_tag"] and r["statut"] not in (PARKED, TERMINAL):
            add("majeur", "doublon_actif", r, f"ligne 🗑️ en statut « {r['statut']} »",
                "passer en En veille ou Refusé / Clos")

    # 8. Inbox : lignes bloquées à une étape depuis plus de 24 h
    for r in inbox_rows or []:
        etape = r.get("Étape") or r.get("etape")
        maj = _d(r.get("Modifié le") or r.get("last_edited") or r.get("cree"))
        if etape in ("Sourcée", "À noter", "Notée", "À briefer", "Briefée") and maj and (today - maj).days >= 1:
            add("majeur", "inbox_bloquee", {"url": r.get("url"), "opportunite": r.get("Titre") or r.get("titre")},
                f"étape « {etape} » depuis {(today - maj).days} j", "l'agent suivant n'a pas tourné : vérifier la base Runs")

    # 9. Runs : un agent planifié sans run aujourd'hui (si la liste des runs est fournie)
    if runs_rows is not None:
        expected = {"Lea_Sourcing", "Hugo_Notation", "Camille_Brief", "Scribe_CRM"}
        if today.weekday() == 6:  # dimanche : pas de chaîne du matin
            expected = set()
        seen = {r.get("Agent") for r in runs_rows if str(r.get("Run", "")).startswith(today.isoformat())}
        for a in sorted(expected - seen):
            add("majeur", "run_manquant", None, f"aucun run de {a} aujourd'hui", "relancer la tâche ou vérifier le connecteur")

    by_status = Counter(r["statut"] for r in rows if not r["doublon_tag"])
    resume = {
        "date": today.isoformat(),
        "lignes": len(rows),
        "lignes_actives": sum(1 for r in rows if not r["doublon_tag"]),
        "par_statut": dict(by_status),
        "dossiers_ouverts": sum(1 for r in rows if r["statut"] in OPEN and not r["doublon_tag"]),
        "problemes": Counter(p["gravite"] for p in problems),
        "par_code": Counter(p["code"] for p in problems),
    }
    return {"resume": resume, "problemes": problems}


def to_markdown(report):
    r = report["resume"]
    lines = [f"# Hygiène du CRM — {r['date']}", "",
             f"{r['lignes']} lignes ({r['lignes_actives']} actives), {r['dossiers_ouverts']} dossiers ouverts.",
             "", "| Statut | Lignes |", "|---|---|"]
    for s in ORDER + [TERMINAL, PARKED]:
        lines.append(f"| {s} | {r['par_statut'].get(s, 0)} |")
    lines += ["", "| Gravité | Nombre |", "|---|---|"]
    for g in ("bloquant", "majeur", "action", "mineur"):
        lines.append(f"| {g} | {r['problemes'].get(g, 0)} |")
    lines += ["", "## Problèmes", ""]
    for p in sorted(report["problemes"], key=lambda p: ("bloquant", "majeur", "action", "mineur").index(p["gravite"])):
        lines.append(f"- **{p['gravite']}** `{p['code']}` — {p['ligne'] or ''} : {p['message']} → {p['correction']}")
    return "\n".join(lines)
