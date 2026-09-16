# -*- coding: utf-8 -*-
"""Ligne de commande : ce que les agents appellent dans leurs prompts.

    python -m pipeline.cli key "Revenue Operations (H/F)" "Dust SAS"
    python -m pipeline.cli seniority annonce.txt --titre "Junior Sales Ops Analyst"
    python -m pipeline.cli links liens.json                  # [{"url": ...}, ...] ou ["url", ...]
    python -m pipeline.cli dedup candidates.json crm.json [inbox.json]
    python -m pipeline.cli validate fichier.json offre|verdict|brief|crm_row|run|evenement_gmail
    python -m pipeline.cli exclusions annonce.txt                       # diplôme d'ingénieur / code exigés (R5, § 1)
    python -m pipeline.cli verdict 16 --titre "Senior Revenue Ops" --annees 5 [--partiel] [--dossier-ouvert] [--grand-groupe] [--crm-admin] [--salaire-max 38000] [--bande stretch]
    python -m pipeline.cli dust-schema verdict                          # Structured Response Format Dust
    python -m pipeline.cli classify sujet.txt corps.txt
    python -m pipeline.cli hygiene crm.json [--inbox inbox.json] [--runs runs.json] [--md]
    python -m pipeline.cli relances crm.json
    python -m pipeline.cli report crm.json --mode soir|pipeline [--pdf out.pdf] [--html out.html]
    python -m pipeline.cli funnel inbox.json [--jours 7] [--reperees N] [--md]
    python -m pipeline.cli runlog --agent Lea_Sourcing --mode production --lues 12 --ecrites 5 --ecartees 7 --erreurs 0 --resume "..." --controles "..."

Toute commande sort du JSON sur stdout et un code retour non nul si une règle est violée.
"""
import argparse
import json
import sys
from datetime import date, datetime


def _paris_now():
    """Horodatage heure de Paris (incident du 07/09/2026 : le conteneur est en UTC, le run était daté 11:34 pour 13:34)."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d %H:%M")


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _print(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1, default=str))


def main(argv=None):
    p = argparse.ArgumentParser(prog="pipeline")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("key"); s.add_argument("titre"); s.add_argument("entreprise")
    s = sub.add_parser("seniority"); s.add_argument("fichier"); s.add_argument("--titre", default="")
    s = sub.add_parser("links"); s.add_argument("fichier")
    s = sub.add_parser("dedup"); s.add_argument("candidates"); s.add_argument("crm"); s.add_argument("inbox", nargs="?")
    s = sub.add_parser("validate"); s.add_argument("fichier"); s.add_argument("schema")
    s = sub.add_parser("classify"); s.add_argument("sujet"); s.add_argument("corps")
    s = sub.add_parser("exclusions"); s.add_argument("fichier")
    s = sub.add_parser("dust-schema"); s.add_argument("schema"); s.add_argument("--out")
    s = sub.add_parser("verdict"); s.add_argument("note", type=int); s.add_argument("--titre", default="")
    s.add_argument("--annees", type=int, default=None); s.add_argument("--partiel", action="store_true")
    s.add_argument("--dossier-ouvert", action="store_true"); s.add_argument("--grand-groupe", action="store_true")
    s.add_argument("--crm-admin", action="store_true"); s.add_argument("--salaire-max", type=int, default=None)
    s.add_argument("--bande", choices=["coeur", "stretch", "inconnu"], default=None)
    s = sub.add_parser("hygiene"); s.add_argument("crm"); s.add_argument("--inbox"); s.add_argument("--runs"); s.add_argument("--md", action="store_true"); s.add_argument("--today")
    s = sub.add_parser("relances"); s.add_argument("crm"); s.add_argument("--today")
    s = sub.add_parser("report"); s.add_argument("crm"); s.add_argument("--mode", default="soir", choices=["soir", "pipeline"]); s.add_argument("--inbox"); s.add_argument("--runs"); s.add_argument("--pdf"); s.add_argument("--html"); s.add_argument("--today")
    s = sub.add_parser("funnel"); s.add_argument("inbox"); s.add_argument("--jours", type=int); s.add_argument("--du"); s.add_argument("--au"); s.add_argument("--reperees", type=int); s.add_argument("--md", action="store_true"); s.add_argument("--today")
    s = sub.add_parser("runlog")
    for a in ("agent", "mode", "resume", "controles"):
        s.add_argument(f"--{a}", required=True)
    for a in ("lues", "ecrites", "ecartees", "erreurs"):
        s.add_argument(f"--{a}", type=int, required=True)
    s.add_argument("--statut", default="OK")
    for a2 in ("reperees", "etudiees", "envoyees"):
        s.add_argument(f"--{a2}", type=int)
    a = p.parse_args(argv)

    if a.cmd == "key":
        from .keys import business_key
        k = business_key(a.entreprise, a.titre)
        _print({"cle": k}); return 0 if k else 1
    if a.cmd == "seniority":
        from .seniority import sourcing_decision
        _print(sourcing_decision(open(a.fichier, encoding="utf-8").read(), a.titre)); return 0
    if a.cmd == "links":
        from .link_check import check
        data = _load(a.fichier)
        urls = [d["url"] if isinstance(d, dict) else d for d in data]
        _print([check(u) for u in urls]); return 0
    if a.cmd == "dedup":
        from .dedup import decide
        out = decide(_load(a.candidates), _load(a.crm), _load(a.inbox) if a.inbox else None)
        _print(out); return 0
    if a.cmd == "validate":
        from .validate import validate_file
        n_ok, errs = validate_file(a.fichier, a.schema)
        _print({"valides": n_ok, "erreurs": errs}); return 1 if errs else 0
    if a.cmd == "classify":
        from .precedence import classify_email
        c = classify_email(open(a.sujet, encoding="utf-8").read(), open(a.corps, encoding="utf-8").read())
        _print(c.__dict__); return 0
    if a.cmd == "exclusions":
        from .exclusions import check
        r = check(open(a.fichier, encoding="utf-8").read())
        _print(r); return 1 if r["exclue"] else 0
    if a.cmd == "dust-schema":
        import pathlib as _p
        from .dust_schema import to_dust
        racine = _p.Path(__file__).resolve().parent.parent
        d = to_dust(_load(str(racine / "schemas" / (a.schema + ".json"))), a.schema)
        txt = json.dumps(d, ensure_ascii=False, indent=1)
        if a.out:
            open(a.out, "w", encoding="utf-8").write(txt)
        print(txt)
        return 0
    if a.cmd == "verdict":
        from .verdicts import verdict
        _print(verdict(a.note, dossier_ouvert=a.dossier_ouvert, titre=a.titre, annees_min=a.annees,
                       texte_partiel=a.partiel, grand_groupe=a.grand_groupe, crm_admin=a.crm_admin,
                       salaire_max=a.salaire_max, bande=a.bande)); return 0
    today = date.fromisoformat(a.today) if getattr(a, "today", None) else date.today()
    if a.cmd == "hygiene":
        from . import hygiene
        rep = hygiene.run(_load(a.crm), today=today, inbox_rows=_load(a.inbox) if a.inbox else None,
                          runs_rows=_load(a.runs) if a.runs else None)
        if a.md:
            print(hygiene.to_markdown(rep))
        else:
            _print(rep)
        return 1 if rep["resume"]["problemes"].get("bloquant") else 0
    if a.cmd == "relances":
        from . import relances
        _print(relances.due(_load(a.crm), today=today)); return 0
    if a.cmd == "report":
        from . import report
        r = report.build(_load(a.crm), mode=a.mode, today=today, inbox_rows=_load(a.inbox) if a.inbox else None,
                         runs_rows=_load(a.runs) if a.runs else None)
        if a.html:
            open(a.html, "w", encoding="utf-8").write(r["html"])
        if a.pdf:
            report.write_pdf(r["html"], a.pdf)
        _print({"stats": r["stats"], "relances": len(r["relances"]), "problemes": r["hygiene"]["resume"]["problemes"],
                "html": a.html, "pdf": a.pdf}); return 0
    if a.cmd == "funnel":
        from . import funnel
        since = date.fromisoformat(a.du) if a.du else (funnel.since_days(a.jours, today) if a.jours is not None else None)
        until = date.fromisoformat(a.au) if a.au else None
        rep = funnel.build(_load(a.inbox), since=since, until=until)
        inv = funnel.check_invariant(a.reperees, rep) if a.reperees is not None else None
        if inv:
            rep["invariant_zero_perte"] = inv
        if a.md:
            print(funnel.to_markdown(rep))
        else:
            _print(rep)
        return 1 if inv and not inv["ok"] else 0
    if a.cmd == "runlog":
        from .validate import errors
        row = {"Run": _paris_now(), "Agent": a.agent, "Mode": a.mode, "Lues": a.lues,
               "Écrites": a.ecrites, "Écartées": a.ecartees, "Erreurs": a.erreurs, "Résumé": a.resume,
               "Contrôles": a.controles, "Statut run": a.statut}
        for k, v in (("Repérées", a.reperees), ("Étudiées", a.etudiees), ("Envoyées à Hugo", a.envoyees)):
            if v is not None:
                row[k] = v
        errs = errors(row, "run")
        _print({"row": row, "erreurs": errs}); return 1 if errs else 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
