import json
import os
from datetime import date

from pipeline import hygiene, relances
from pipeline.dedup import decide, find_duplicates

HERE = os.path.dirname(__file__)
EXPORT = os.path.join(os.path.dirname(HERE), "data", "crm_export_2026-09-07.json")


def crm():
    with open(EXPORT, encoding="utf-8") as f:
        return json.load(f)


def test_real_export_loads():
    rows = crm()
    assert len(rows) >= 200


def test_dedup_against_real_base():
    cands = [
        {"titre": "Revenue Operations", "entreprise": "Dust", "lien_direct": "https://x/1"},
        {"titre": "Growth Ops Analyst", "entreprise": "Entreprise Inconnue XYZ", "lien_direct": "https://x/2"},
        {"titre": "Growth Ops Analyst (H/F)", "entreprise": "Entreprise Inconnue XYZ SAS", "lien_direct": "https://x/3"},
    ]
    out = decide(cands, crm())
    assert out[0]["decision"] == "doublon_crm"
    assert out[1]["decision"] == "nouvelle"
    assert out[2]["decision"] == "doublon_lot"          # même clé dans le lot du jour


def test_find_duplicates_ignores_tagged_rows():
    dups = find_duplicates(crm())
    for k, grp in dups.items():
        assert all(not str(r["Opportunité"]).startswith("🗑️") for r in grp)


def test_hygiene_runs_on_real_export():
    rep = hygiene.run(crm(), today=date(2026, 9, 7))
    assert rep["resume"]["lignes"] >= 200
    codes = rep["resume"]["par_code"]
    assert "score_manquant" in codes           # constat connu de l'audit du 02/09
    assert rep["resume"]["problemes"].get("bloquant", 0) == 0


def test_relances_are_only_for_open_files():
    dues = relances.due(crm(), today=date(2026, 9, 7))
    assert all(d["statut"] in hygiene.OPEN for d in dues)
    assert dues == sorted(dues, key=lambda d: (d["priorite"], -d["retard_jours"]))


def test_hygiene_flags_tagged_duplicate_in_active_status():
    rows = [{"url": "u1", "Opportunité": "🗑️ DOUBLON — RevOps — Acme", "Statut": "Entretien", "Score /20": 15, "cree": "2026-09-01"}]
    rep = hygiene.run(rows, today=date(2026, 9, 7))
    assert "doublon_actif" in rep["resume"]["par_code"]


def test_hygiene_detects_missing_run():
    rep = hygiene.run([], today=date(2026, 9, 8), runs_rows=[{"Run": "2026-09-08 07:31", "Agent": "Lea_Sourcing"}])
    missing = {p["message"] for p in rep["problemes"] if p["code"] == "run_manquant"}
    assert any("Hugo_Notation" in m for m in missing) and not any("Lea_Sourcing" in m for m in missing)


def test_notee_nest_pas_bloquee():
    # Incident du 14/09/2026 : « Notée » (dossier déjà ouvert) est une étape terminale
    import datetime as dt
    from pipeline import hygiene
    today = dt.date(2026, 9, 14)
    inbox = [{"url": "u1", "Titre": "X — Qonto", "Étape": "Notée", "Modifié le": "2026-09-10"},
             {"url": "u2", "Titre": "Y — Joko", "Étape": "À briefer", "Modifié le": "2026-09-09"}]
    rep = hygiene.run([], today=today, inbox_rows=inbox)
    bloquees = [p["url"] for p in rep["problemes"] if p["code"] == "inbox_bloquee"]
    assert bloquees == ["u2"]
