# -*- coding: utf-8 -*-
"""Entonnoir de Léa : combien d'offres elle étudie, combien elle envoie à Hugo, pourquoi elle écarte les autres,
et ce que Hugo fait de celles qu'elle envoie (précision du sourcing).

Source unique : l'export de l'Inbox. La règle zéro perte de Léa garantit qu'une offre étudiée = une ligne Inbox,
écartées et doublons compris. Une offre « envoyée à Hugo » est une ligne passée par « À noter » : elle y est
encore, ou elle porte un verdict / une note, ou elle attend en veille au-delà du plafond.
"""
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

APRES_HUGO = {"À briefer", "Briefée", "Notée", "Transférée", "Au CRM"}
MOTIFS = [
    ("seniorite", r"> ?5 ans|ans demandés|ans d'expérience|séniorité|senior"),
    ("offre_fermee", r"fermée|lien mort|expirée|plus disponible|404"),
    ("exclusion_technique", r"diplôme|ingénieur|informatique|\bcode\b|python|langchain|aws|r16|data scien|software|ml\b"),
    ("prospection", r"outbound|prospection|cold call|chasse|business developer|sdr\b"),
    ("contrat", r"\bcdd\b|stage|alternance|freelance|interim|intérim|mission|pas un cdi"),
    ("geographie", r"trajet|lieu|localisation|géograph|hors (paris|idf|île|france)|relocation|étranger"),
    ("hors_perimetre", r"hors (périmètre|cible|famille)|famille|pas un poste|hors opérations"),
    ("deja_refuse", r"déjà refusé|refus"),
]


def _g(r, *names):
    for n in names:
        if r.get(n) not in (None, ""):
            return r[n]
    return None


def _day(r):
    v = _g(r, "Run sourcing", "date:Run sourcing:start", "run_sourcing", "Créé le", "createdTime", "cree")
    if not v:
        return None
    s = str(v)
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
        except ValueError:
            return None


def motif(raison):
    t = (raison or "").lower()
    for code, rx in MOTIFS:
        if re.search(rx, t):
            return code
    return "autre"


def classify(r):
    """Retourne (sort_lea, issue_hugo)."""
    etape = _g(r, "Étape", "etape") or ""
    raison = _g(r, "Raison", "raison") or ""
    verdict = _g(r, "Verdict", "verdict")
    score = _g(r, "Score agent", "score_agent")
    if etape == "Calibration":
        return "calibration", None
    if etape == "Doublon":
        return "doublon", None
    if etape == "Erreur" and not verdict:
        return "erreur", None
    if etape == "En veille" and str(raison).lower().startswith("au-delà du plafond") and not verdict:
        return "envoyee", "en_attente_plafond"
    if etape == "À noter":
        return "envoyee", "en_attente"
    if verdict or score is not None or etape in APRES_HUGO:
        return "envoyee", (verdict or ("go_prioritaire" if etape in APRES_HUGO else "notee"))
    if etape == "Écartée":
        return "ecartee", None
    return "autre", None


def build(inbox_rows, since=None, until=None):
    rows = []
    for r in inbox_rows:
        d = _day(r)
        if since and (d is None or d < since):
            continue
        if until and (d is None or d > until):
            continue
        rows.append((d, r))
    tot = Counter(); motifs = Counter(); hugo = Counter(); familles = defaultdict(Counter); sources = defaultdict(Counter)
    par_jour = defaultdict(Counter)
    for d, r in rows:
        sort_lea, issue = classify(r)
        tot["etudiees"] += 1
        tot[sort_lea] += 1
        jour = d.isoformat() if d else "sans date"
        par_jour[jour]["etudiees"] += 1
        par_jour[jour][sort_lea] += 1
        fam = _g(r, "Famille", "famille") or "?"
        src = _g(r, "Source", "source") or "?"
        familles[fam]["etudiees"] += 1; sources[src]["etudiees"] += 1
        if sort_lea == "envoyee":
            hugo[issue] += 1
            familles[fam]["envoyees"] += 1; sources[src]["envoyees"] += 1
            if issue == "go_prioritaire":
                par_jour[jour]["go"] += 1
        if sort_lea == "ecartee":
            motifs[motif(_g(r, "Raison", "raison"))] += 1
    env = tot["envoyee"]
    notees = sum(v for k, v in hugo.items() if k not in ("en_attente", "en_attente_plafond"))
    go = hugo.get("go_prioritaire", 0)
    return {
        "periode": {"du": since.isoformat() if since else None, "au": until.isoformat() if until else None},
        "etudiees": tot["etudiees"],
        "envoyees_a_hugo": env,
        "ecartees_par_lea": tot["ecartee"],
        "doublons": tot["doublon"],
        "erreurs": tot["erreur"],
        "calibration": tot["calibration"],
        "taux_envoi": round(env / tot["etudiees"], 3) if tot["etudiees"] else None,
        "motifs_ecart": dict(motifs.most_common()),
        "issue_chez_hugo": dict(hugo),
        "precision_lea": round(go / notees, 3) if notees else None,
        "par_jour": {k: dict(v) for k, v in sorted(par_jour.items())},
        "par_famille": {k: dict(v) for k, v in familles.items()},
        "par_source": {k: dict(v) for k, v in sources.items()},
    }


def check_invariant(reperees, report):
    """Zéro perte : toute offre repérée par Léa pendant le run doit avoir sa ligne Inbox."""
    return {"reperees": reperees, "lignes": report["etudiees"], "ok": reperees == report["etudiees"],
            "manquantes": max(0, reperees - report["etudiees"])}


def to_markdown(rep):
    L = [f"# Entonnoir de Léa ({rep['periode']['du'] or 'début'} → {rep['periode']['au'] or 'aujourd’hui'})", "",
         f"- Offres étudiées : **{rep['etudiees']}**",
         f"- Envoyées à Hugo : **{rep['envoyees_a_hugo']}** (taux {'' if rep['taux_envoi'] is None else round(rep['taux_envoi']*100)} %)",
         f"- Écartées par Léa : {rep['ecartees_par_lea']} · doublons : {rep['doublons']} · erreurs : {rep['erreurs']}",
         f"- Précision de Léa (go prioritaire / offres notées par Hugo) : "
         f"{'n/a' if rep['precision_lea'] is None else str(round(rep['precision_lea']*100)) + ' %'}", "",
         "| Jour | Étudiées | Envoyées | Écartées | Doublons | Go Hugo |", "|---|---|---|---|---|---|"]
    for j, c in rep["par_jour"].items():
        L.append(f"| {j} | {c.get('etudiees',0)} | {c.get('envoyee',0)} | {c.get('ecartee',0)} | {c.get('doublon',0)} | {c.get('go',0)} |")
    L += ["", "| Motif d'écart | Nombre |", "|---|---|"] + [f"| {k} | {v} |" for k, v in rep["motifs_ecart"].items()]
    L += ["", "| Issue chez Hugo | Nombre |", "|---|---|"] + [f"| {k} | {v} |" for k, v in rep["issue_chez_hugo"].items()]
    return "\n".join(L)


def since_days(n, today=None):
    today = today or date.today()
    return today - timedelta(days=n)
