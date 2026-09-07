from pipeline.seniority import band, sourcing_decision, years_required


def test_ranges():
    assert years_required("3 à 5 ans d'expérience") == (3, 5)
    assert years_required("2-4 years of experience in RevOps") == (2, 4)


def test_minimum_and_plus():
    assert years_required("at least 2 years") == (2, 2)
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
