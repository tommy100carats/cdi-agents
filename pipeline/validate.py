# -*- coding: utf-8 -*-
"""Validation JSON Schema de tout ce qu'un agent veut écrire.

Un agent ne colle jamais une propriété dans Notion à partir de sa tête : il écrit un fichier JSON,
`validate` le refuse ou l'accepte, et seul un fichier accepté est écrit. C'est ce qui a manqué en
v1 (33 fiches sans score sur 199).
"""
import json
import os

from jsonschema import Draft202012Validator

SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schemas")
_CACHE = {}


def load_schema(name: str) -> dict:
    if name not in _CACHE:
        with open(os.path.join(SCHEMA_DIR, f"{name}.json"), encoding="utf-8") as f:
            _CACHE[name] = json.load(f)
    return _CACHE[name]


def errors(obj, schema_name: str):
    """Liste (vide si valide) de messages « chemin : problème », triés."""
    v = Draft202012Validator(load_schema(schema_name))
    out = []
    for e in sorted(v.iter_errors(obj), key=lambda e: list(e.path)):
        path = "/".join(str(p) for p in e.path) or "(racine)"
        out.append(f"{path} : {e.message}")
    return out


def is_valid(obj, schema_name: str) -> bool:
    return not errors(obj, schema_name)


def validate_file(path: str, schema_name: str):
    """Valide un fichier contenant un objet ou une liste d'objets. Retourne (n_ok, erreurs)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = data if isinstance(data, list) else [data]
    all_errors = []
    n_ok = 0
    for i, obj in enumerate(items):
        errs = errors(obj, schema_name)
        if errs:
            all_errors.extend([f"[{i}] {e}" for e in errs])
        else:
            n_ok += 1
    return n_ok, all_errors
