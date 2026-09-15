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
    assert band("no years stated", "Senior Sales Operations Manager")["band"] == "stretch"  # senior sans années = 5 ans, au cas où (R2)
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
    assert band(body)["band"] == "stretch"
    assert years_required("Fondée il y a 3 ans, l'entreprise recrute. Aucune expérience requise.") == (None, None)


def test_duree_de_conservation_des_donnees_ignoree():
    # Incident du 10/09/2026 (Qonto)
    from pipeline.seniority import band
    txt = "Customer Success & Development Manager. Your data is kept for up to 2 years after the process."
    assert band(txt, "Customer Success & Development Manager")["band"] == "inconnu"
