from pipeline.keys import business_key, key_from_opportunite, normalize_company, normalize_title, split_opportunite


def test_same_offer_two_sources_same_key():
    a = business_key("Dust SAS", "Revenue Operations (H/F)")
    b = business_key("dust", "Revenue Operations")
    assert a == b == "dust|revenue operations"


def test_gender_and_contract_markers_removed():
    assert normalize_title("Sales Operations Analyst H/F - CDI") == "sales operations analyst"
    assert normalize_title("Knowledge & Bot manager (H/F/X)") == "knowledge and bot manager"


def test_seniority_words_kept():
    assert normalize_title("Junior RevOps Analyst") != normalize_title("RevOps Analyst")


def test_company_aliases_and_noise():
    assert normalize_company("AVIV Group") == "seloger"
    assert normalize_company("Numberly (groupe 1000mercis)") == normalize_company("Numberly")
    assert normalize_company("Pennylane France SAS") == "pennylane"


def test_split_opportunite_and_doublon_prefix():
    assert split_opportunite("Revenue Operations — Dust") == ("Revenue Operations", "Dust")
    assert key_from_opportunite("🗑️ DOUBLON — Revenue Operations — Dust") == "dust|revenue operations"


def test_empty_parts_give_empty_key():
    assert business_key("", "RevOps") == ""
    assert key_from_opportunite("Titre sans entreprise") == ""


def test_title_location_suffixes_are_ignored():
    # Incident du 07/09/2026 : variantes de titre avec lieu ou sous-titre
    assert business_key("Figma", "Customer Enablement Manager (Paris, France)") == business_key("Figma", "Customer Enablement Manager")
    assert business_key("Mirakl", "Revenue Operations Analyst, Paris") == business_key("Mirakl", "Revenue Operations Analyst")
    assert business_key("ElevenLabs", "Chief of Staff GTM - France") == business_key("ElevenLabs", "Chief of Staff GTM")
    assert business_key("Doctolib", "Sales Operations Lead (x/f/m)") == business_key("Doctolib", "Sales Operations Lead")
    # mais un vrai qualificatif reste distinct
    assert business_key("Brevo", "Senior Sales Operations Manager") != business_key("Brevo", "Sales Operations Manager")


def test_region_en_fin_de_titre_sans_virgule():
    # Incident du 09/09/2026 (Aircall)
    from pipeline.keys import business_key
    a = business_key("Aircall", "Senior Revenue Operations Business Partner, EMEA")
    b = business_key("Aircall", "Senior Revenue Operations Business Partner EMEA")
    assert a == b and a.endswith("business partner")
