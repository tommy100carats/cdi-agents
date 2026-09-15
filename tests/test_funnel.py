# -*- coding: utf-8 -*-
from datetime import date
from pipeline import funnel

ROWS = [
    {"Étape": "À noter", "Run sourcing": "2026-09-14 07:30", "Famille": "RevOps", "Source": "Ashby"},
    {"Étape": "Écartée", "Raison": "> 5 ans demandés", "Run sourcing": "2026-09-14 07:30"},
    {"Étape": "Écartée", "Raison": "offre fermée, preuve : 404", "Run sourcing": "2026-09-14 07:30"},
    {"Étape": "Écartée", "Verdict": "no_go", "Score agent": 9, "Raison": "note basse", "Run sourcing": "2026-09-14 07:30"},
    {"Étape": "Briefée", "Verdict": "go_prioritaire", "Score agent": 16, "Run sourcing": "2026-09-15 07:30"},
    {"Étape": "Doublon", "Run sourcing": "2026-09-15 07:30"},
    {"Étape": "En veille", "Raison": "au-delà du plafond du run", "Run sourcing": "2026-09-15 07:30"},
    {"Étape": "À noter", "Run sourcing": "2026-08-01 07:30"},
]


def test_entonnoir_compte_etudiees_et_envoyees():
    r = funnel.build(ROWS, since=date(2026, 9, 14))
    assert r["etudiees"] == 7
    assert r["envoyees_a_hugo"] == 4          # à noter, no_go noté, briefée, plafond
    assert r["ecartees_par_lea"] == 2
    assert r["doublons"] == 1
    assert r["motifs_ecart"] == {"seniorite": 1, "offre_fermee": 1}
    assert r["precision_lea"] == 0.5          # 1 go sur 2 notées


def test_invariant_zero_perte():
    r = funnel.build(ROWS, since=date(2026, 9, 15))
    assert funnel.check_invariant(3, r)["ok"]
    assert funnel.check_invariant(5, r)["manquantes"] == 2
