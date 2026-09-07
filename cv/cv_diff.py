#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cv_diff.py : ce qui a changé entre le CV de référence et un CV ciblé.

    python3 cv/cv_diff.py cv/cv_reference_en.py cv/cv_data_dust_en.py

Sort, pour chaque champ, la référence et la version ciblée quand elles diffèrent. Tom ne relit que le
diff, pas le CV entier : c'est ce qui rend la validation humaine tenable à raison d'un CV par jour.
Une expérience ajoutée ou un chiffre nouveau apparaissent ici en clair : ce sont des inventions à refuser.
"""
import importlib.util
import re
import sys


def load(path):
    spec = importlib.util.spec_from_file_location("cfg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.DATA


def strip(s):
    return re.sub(r"<[^>]+>", "", str(s)).replace("&amp;", "&")


def flatten(d):
    out = {}
    for k in ("out", "titre", "profil", "t_profil", "t_xp", "t_asso"):
        out[k] = strip(d.get(k, ""))
    for titre, items in d.get("sidebar", []):
        out[f"sidebar/{strip(titre)}"] = " | ".join(strip(i) for i in items)
    for x in d.get("experiences", []):
        key = f"xp/{strip(x.get('boite'))}"
        out[key + "/poste"] = strip(x.get("poste", ""))
        out[key + "/dates"] = strip(x.get("dates", ""))
        out[key + "/activite"] = strip(x.get("activite", ""))
        out[key + "/puces"] = "\n    ".join(strip(p) for p in x.get("puces", []))
    out["projets"] = "\n    ".join(strip(p) for p in d.get("projets", []))
    return out


def numbers(s):
    return set(re.findall(r"\d[\d\s,\.]*\s?(?:M€|k€|K|M|%|€)?", s))


def main(ref_path, new_path):
    ref, new = flatten(load(ref_path)), flatten(load(new_path))
    keys = list(dict.fromkeys(list(ref) + list(new)))
    changed = 0
    for k in keys:
        a, b = ref.get(k, ""), new.get(k, "")
        if a != b:
            changed += 1
            print(f"## {k}")
            print(f"  référence : {a[:600]}")
            print(f"  ciblé     : {b[:600]}")
            new_nums = numbers(b) - numbers(a)
            if new_nums and k.startswith(("xp/", "projets", "profil")):
                print(f"  ⚠️ chiffres absents de la référence : {sorted(new_nums)} (à justifier par rules/profil.md)")
            print()
    added_xp = {k.split('/')[1] for k in new if k.startswith('xp/')} - {k.split('/')[1] for k in ref if k.startswith('xp/')}
    if added_xp:
        print(f"⛔ expériences absentes de la référence : {sorted(added_xp)} (invention probable)")
    print(f"{changed} champ(s) modifié(s) sur {len(keys)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
