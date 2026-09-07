import json
import os
from datetime import date

from pipeline import report
from pipeline.validate import errors

HERE = os.path.dirname(__file__)
EXPORT = os.path.join(os.path.dirname(HERE), "data", "crm_export_2026-09-07.json")


def test_crm_row_requires_score():
    row = {"Opportunité": "RevOps — Acme", "Poste": "RevOps", "Statut": "À contacter", "Type de contrat": "CDI",
           "Rôle cible": "RevOps", "Répond aux critères": "Oui", "Source": "LinkedIn", "Lien offre": "https://acme.com/j/1",
           "Fit — pourquoi c'est pour toi": "x" * 50, "Priorité": "Haute", "Clé": "acme|revops",
           "Écrit par": "Scribe_CRM", "Run": "2026-09-07 09:15"}
    assert any("Score /20" in e for e in errors(row, "crm_row"))
    row["Score /20"] = 16
    assert errors(row, "crm_row") == []
    row["Score /20"] = 25
    assert errors(row, "crm_row")


def test_verdict_schema_bounds():
    v = {"cle": "acme|revops", "entreprise": "Acme", "poste": "RevOps", "famille": "RevOps", "dossier_deja_ouvert": False,
         "couverture": [{"exigence": "HubSpot", "preuve": "certifié", "etat": "partiel", "centrale": True}],
         "score_couverture_10": 6, "score_conditions_3": 2, "score_entreprise_4": 3, "score_differenciateurs_3": 1,
         "note_20": 12, "verdict": "veille", "raison_principale": "couverture partielle des exigences", "exigences_sans_preuve": [],
         "deductions": "", "detail": "une ligne par exigence, ici une seule", "regles_appliquees": ["R4"], "run": "2026-09-07 08:15"}
    assert errors(v, "verdict") == []
    v["note_20"] = 21
    assert errors(v, "verdict")


def test_run_schema():
    r = {"Run": "2026-09-07 07:31", "Agent": "Lea_Sourcing", "Mode": "calibration", "Lues": 40, "Écrites": 20,
         "Écartées": 20, "Erreurs": 0, "Résumé": "20 offres proposées pour calibration", "Contrôles": "liens 20/20 vérifiés",
         "Statut run": "OK"}
    assert errors(r, "run") == []


def test_report_builds_html_and_stats():
    with open(EXPORT, encoding="utf-8") as f:
        rows = json.load(f)
    r = report.build(rows, mode="pipeline", today=date(2026, 9, 7))
    assert "<h1>" in r["html"] and r["stats"]["ouverts"] >= 1
    r2 = report.build(rows, mode="soir", today=date(2026, 9, 7))
    assert "Dossiers ouverts" in r2["html"]
