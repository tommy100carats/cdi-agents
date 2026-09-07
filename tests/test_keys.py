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
