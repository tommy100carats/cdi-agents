import json
import pathlib

from pipeline.dust_schema import to_dust

RACINE = pathlib.Path(__file__).resolve().parent.parent


def _schema(nom):
    return json.loads((RACINE / "schemas" / f"{nom}.json").read_text(encoding="utf-8"))


def test_toutes_les_proprietes_sont_requises_mode_strict():
    # Dust refuse un schéma strict où une propriété n'est pas dans required (incident de migration 07/09)
    for nom in ("verdict", "offre", "crm_row", "brief", "evenement_gmail", "run"):
        s = to_dust(_schema(nom), nom)["json_schema"]["schema"]
        assert set(s["properties"]) == set(s["required"]), nom
        assert s["additionalProperties"] is False, nom


def test_une_propriete_optionnelle_devient_nullable():
    s = to_dust(_schema("offre"), "offre")["json_schema"]["schema"]
    src = _schema("offre")
    optionnelle = next(p for p in src["properties"] if p not in src["required"])
    assert "null" in s["properties"][optionnelle]["type"]


def test_les_mots_cles_non_supportes_sont_retires():
    s = to_dust(_schema("verdict"), "verdict")["json_schema"]["schema"]
    assert "minLength" not in s["properties"]["cle"]
    assert "$schema" not in s and "title" not in s


def test_le_nom_dust_et_l_enveloppe():
    d = to_dust(_schema("verdict"), "verdict")
    assert d["type"] == "json_schema"
    assert d["json_schema"]["name"] == "verdict_offre"
    assert d["json_schema"]["strict"] is True


def test_les_enums_et_la_couverture_survivent():
    s = to_dust(_schema("verdict"), "verdict")["json_schema"]["schema"]
    assert "go_prioritaire" in s["properties"]["verdict"]["enum"]
    item = s["properties"]["couverture"]["items"]
    assert set(item["properties"]) == {"exigence", "preuve", "etat", "centrale"}
    assert item["additionalProperties"] is False


def test_cv_data_json_devient_un_fichier_cv_data():
    # Inès rend un JSON ; le fichier .py est produit par du code, jamais recopié à la main (07/09)
    import sys
    sys.path.insert(0, str(RACINE))
    from cv.cv_data_from_json import build
    data = {"cible": "Dust", "lang": "fr", "titre": "Revenue Operations", "ouverture": "structuration",
            "profil": "x" * 90,
            "sidebar": [{"section": "Outils", "lignes": ["HubSpot (certifié)"]}],
            "experiences": [{"poste": "Responsable", "boite": "CITYZ", "dates": "2023-2026",
                             "activite": "Formation", "puces": ["a"]}],
            "projets": ["Mentalizi"], "cartographie": [{"exigence": "HubSpot", "preuve": "certifié"}],
            "a_verifier": ["Salesforce"], "run": "2026-09-07 16:00"}
    out = build(data)
    assert out["out"] == "CV Tom Antonietti Dust.pdf"
    assert out["titre"] == "Revenue Operations"
    assert out["sidebar"][0] == ("Outils", ["HubSpot (certifié)"])
    # la maquette vient de la référence, l'agent n'y touche pas
    assert out["nom"] and out["contacts"] and out["photo"]
