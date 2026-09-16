from pipeline.exclusions import check, engineer_degree_required
from pipeline.verdicts import hors_operations, senior_cap, verdict


def test_thresholds_from_tom():
    assert verdict(15)["verdict"] == "go_prioritaire"
    assert verdict(14)["verdict"] == "veille"
    assert verdict(12)["verdict"] == "veille"
    assert verdict(11)["verdict"] == "no_go"
    assert verdict(16, dossier_ouvert=True)["verdict"] == "dossier_ouvert"


def test_senior_cap_r13():
    # Alan « Senior Revenue Ops », 5 ans demandés : Tom a dit non (13/20, « pas assez d'expérience »)
    v = verdict(18, titre="Senior Revenue Ops", annees_min=5)
    assert v["verdict"] == "veille" and v["plafonne"] and v["note"] == 18
    # « Senior » sans années écrites, ou 4 ans : pas de plafond (Cegid, Tom a dit oui)
    # R17 (16/09/2026) : un titre senior est plafonné, sauf si 3 ans ou moins sont écrits
    assert senior_cap("Senior sales operations specialist", None)
    assert senior_cap("Senior sales operations specialist", 4)
    assert not senior_cap("Senior sales operations specialist", 3)
    # Lead + 5 à 8 ans (Mistral) : plafonné, Tom à 14 « un peu junior »
    assert senior_cap("Enablement Lead, Programs", 5)
    # Responsable Sales Operations, 4 ans : pas senior au sens du titre
    assert not senior_cap("Responsable Sales Operations", 4)


def test_hors_ops_cap_r14():
    for t in ("Product Manager Officer Comptabilité et IA F/H", "Business Analyst IA H/F", "Consultant IA (H/F)",
              "AI SOLUTIONS PRODUCT OWNER - Domaine OFFRES", "AI Transformation Senior H/F",
              "Fullstack Software Engineer (x/f/m)"):
        assert hors_operations(t), t
    for t in ("Revenue Operations Analyst, Paris", "Strategy & Operations Analyst", "Compliance Ops Builder",
              "Customer Success Manager", "Deal Desk Analyst F/H", "Sales Analyst & Support (F/H/X) - CDI",
              "Chief of Staff GTM - France", "Player Experience Specialist (AI & Automation)"):
        assert hors_operations(t) is None, t
    v = verdict(16, titre="Business Analyst IA H/F")
    assert v["verdict"] == "veille" and "R14" in v["plafonds"][0]


def test_partial_text_cap_r15_and_note_untouched():
    v = verdict(15, titre="Chief of Staff GTM - France", texte_partiel=True)
    assert v["verdict"] == "veille" and v["note"] == 15
    # un plafond ne relève jamais un no_go
    assert verdict(9, texte_partiel=True)["verdict"] == "no_go"


def test_engineer_degree_exclusion_meilleurtaux():
    txt = "Formation : Bac +5 École d'Ingénieurs ou Master Informatique avec spécialisation Intelligence Artificielle."
    assert engineer_degree_required(txt)
    assert check(txt)["exclue"]


def test_degree_with_business_alternative_passes():
    txt = "Diplômé(e) d'une école de commerce ou d'ingénieurs, vous avez 2 ans d'expérience en opérations."
    assert engineer_degree_required(txt) is None
    assert not check("Vous êtes curieux des outils d'automatisation et de l'IA appliquée.")["exclue"]


def test_code_core_exclusion():
    assert check("Maîtrise de LangChain et des pipelines de données en production exigée.")["exclue"]
    assert not check("Vous avez entendu parler de LangChain, c'est un plus.")["exclue"]


def test_regles_du_16_09():
    # R19 : grand groupe coté, seuil go à 13
    assert verdict(13)["verdict"] == "veille"
    assert verdict(13, grand_groupe=True)["verdict"] == "go_prioritaire"
    # R18 : administration CRM en production exigée
    v = verdict(17, crm_admin=True)
    assert v["verdict"] == "veille" and v["plafonne"]
    # R20 : salaire affiché sous 40 k€
    assert verdict(18, salaire_max=38000)["verdict"] == "no_go"
    assert verdict(15, salaire_max=45000)["verdict"] == "go_prioritaire"


def test_stretch_plafonne_sauf_grand_groupe():
    assert verdict(16, bande="stretch")["verdict"] == "veille"
    assert verdict(16, bande="stretch", grand_groupe=True)["verdict"] == "go_prioritaire"
    assert verdict(16, bande="coeur")["verdict"] == "go_prioritaire"
