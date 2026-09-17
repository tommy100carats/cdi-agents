from pipeline.seniority import band, sourcing_decision, years_required


def test_ranges():
    assert years_required("3 à 5 ans d'expérience") == (3, 5)
    assert years_required("2-4 years of experience in RevOps") == (2, 4)


def test_minimum_and_plus():
    assert years_required("at least 2 years") == (2, None)  # « au moins » = pas de borne haute (07/09)
    assert years_required("5+ years") == (5, None)


def test_bands_per_tom_rules():
    assert band("2 ans d'expérience")["band"] == "coeur"
    assert band("3 à 5 ans")["band"] == "coeur"          # borne basse 3 = coeur
    assert band("minimum 4 ans")["band"] == "stretch"
    assert band("minimum 5 ans d'expérience")["band"] == "hors"   # R17 (16/09/2026)
    assert band("8+ years")["band"] == "hors"
    assert band("aucune mention")["band"] == "inconnu"


def test_decision_keeps_unknown_and_stretch_rejects_hors():
    assert sourcing_decision("4 years")["keep"]
    assert sourcing_decision("no experience stated")["keep"]
    assert not sourcing_decision("7 ans minimum")["keep"]


def test_level_words_only_in_title_not_in_body():
    # Incident du 07/09/2026 : « leadership » dans le corps classait un poste Junior en « hors »
    body = "You will work with leadership and the senior team. First experience in Sales Operations."
    assert band(body, "Junior Sales Operations Analyst")["band"] == "coeur"
    assert band(body)["band"] == "inconnu"
    assert band("no years stated", "Senior Sales Operations Manager")["band"] == "hors"  # R17 : senior sans années = hors
    assert band("no years stated", "Head of Revenue Operations")["band"] == "hors"
    assert band("no years stated", "Sales Operations Lead")["band"] == "hors"
    assert band("no years stated", "Revenue Operations Analyst")["band"] == "inconnu"
    # les années écrites priment sur le titre
    assert band("2 ans d'expérience", "Senior RevOps")["band"] == "coeur"


def test_years_outside_experience_context_are_ignored():
    # Incident du 07/09/2026 : RGPD en pied d'annonce et âge de l'entreprise
    body = ("In 6 years of existence we raised a lot. 5+ years of experience in Strategy & Operations. "
            "Si votre candidature n'aboutit pas, vos données peuvent être conservées 2 ans.")
    assert years_required(body) == (5, None)
    assert band(body)["band"] == "hors"   # R17 : 5 ans et plus = hors
    assert years_required("Fondée il y a 3 ans, l'entreprise recrute. Aucune expérience requise.") == (None, None)


def test_duree_de_conservation_des_donnees_ignoree():
    # Incident du 10/09/2026 (Qonto)
    from pipeline.seniority import band
    txt = "Customer Success & Development Manager. Your data is kept for up to 2 years after the process."
    assert band(txt, "Customer Success & Development Manager")["band"] == "inconnu"


def test_corrections_du_17_09():
    # durée qui décrit une personne (Qonto)
    assert years_required("Our Head of Pricing: she spent 15+ years in fintech. You have 2 years of experience in pricing.") == (2, 2)
    # 8/10 ans et 5-7 années (Pennylane, Digitrips)
    assert years_required("Vous avez 8/10 ans d'expérience en Strategy & Ops") == (8, 10)
    assert years_required("5-7 années d'expérience") == (5, 7)
    # nombres en lettres (NHCO)
    assert band("Vous justifiez de cinq ans d'expérience en contrôle de gestion")["band"] == "hors"
    assert years_required("at least three years of experience") == (3, None)
    # plusieurs exigences : la plus grande compte
    assert years_required("Minimum de 2 ans en management. 5 ans d'expérience en pilotage commercial.")[0] == 5
    # une durée « appréciée » ne remonte pas le minimum
    assert years_required("2 ans d'expérience en Sales Ops. 5 ans en SaaS serait un plus.")[0] == 2
    # « un an » ne casse pas les mots
    assert years_required("Une première expérience d'un an minimum en opérations")[0] == 1
