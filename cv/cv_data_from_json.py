#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convertit un cv_data JSON (sortie structurée d'Inès) en fichier cv_data_<cible>.py.

    python3 cv/cv_data_from_json.py cv.json > cv/cv_data_dust_fr.py

Le JSON est d'abord validé contre schemas/cv_data.json : un JSON refusé ne devient jamais un fichier.
Les champs de maquette (nom, contacts, photo, titres de sections) viennent du CV de référence :
l'agent ne les produit pas, il n'a pas à y toucher.
"""
import json
import sys
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))


def build(data: dict) -> dict:
    """Assemble la structure DATA attendue par cv/cv_build.py."""
    ref = "cv_reference_en" if data["lang"] == "en" else "cv_reference_fr"
    module = __import__(f"cv.{ref}", fromlist=["DATA"])
    out = dict(module.DATA)
    out["out"] = f"CV Tom Antonietti {data['cible']}.pdf"
    out["titre"] = data["titre"]
    out["profil"] = data["profil"]
    out["sidebar"] = [(s["section"], s["lignes"]) for s in data["sidebar"]]
    out["experiences"] = [dict(e) for e in data["experiences"]]
    out["projets"] = list(data["projets"])
    return out


def main(argv):
    from pipeline.validate import errors
    data = json.loads(pathlib.Path(argv[1]).read_text(encoding="utf-8"))
    errs = errors(data, "cv_data")
    if errs:
        sys.stderr.write("cv_data refusé par le schéma :\n" + "\n".join(errs) + "\n")
        return 1
    sys.stdout.write("# -*- coding: utf-8 -*-\n# Généré depuis " + argv[1] + ", ne pas éditer à la main.\n")
    sys.stdout.write("DATA = " + repr(build(data)) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
