# -*- coding: utf-8 -*-
"""Conversion des schémas du dépôt en « Structured Response Format » Dust.

Migration du 07/09/2026 : les agents Dust imposent leur sortie par un JSON Schema en mode strict.
Le schéma collé dans Dust n'est jamais retapé à la main : il est produit ici depuis `schemas/*.json`,
qui reste la source de vérité. Deux différences imposées par le mode strict :

- toute propriété doit figurer dans `required` ; une propriété optionnelle devient donc nullable ;
- les mots-clés de validation fine (minLength, pattern, minItems...) ne sont pas supportés et sont
  retirés. Ils restent appliqués par `pipeline.cli validate`, qui garde le dernier mot : Dust cadre
  la forme, le dépôt valide le fond.
"""
import copy

_DROP = {"minLength", "maxLength", "minimum", "maximum", "format", "pattern", "minItems",
         "maxItems", "$schema", "title", "default", "examples", "uniqueItems", "const"}

NOMS = {"verdict": "verdict_offre", "brief": "brief_entreprise", "offre": "offre_sourcee",
        "crm_row": "fiche_crm", "evenement_gmail": "evenement_gmail", "run": "ligne_run"}


def _nullable(t):
    if isinstance(t, str):
        return [t, "null"] if t != "null" else t
    if isinstance(t, list):
        return t if "null" in t else t + ["null"]
    return t


def _clean(node, optionnelle=False):
    if not isinstance(node, dict):
        return node
    out = {k: v for k, v in node.items() if k not in _DROP}
    if optionnelle and "enum" in out and None not in out["enum"]:
        out["enum"] = list(out["enum"]) + [None]
    if optionnelle and "type" in out:
        out["type"] = _nullable(out["type"])
    if out.get("properties"):
        requises = set(node.get("required", []))
        out["properties"] = {n: _clean(s, optionnelle=(n not in requises))
                             for n, s in out["properties"].items()}
        out["required"] = list(out["properties"])
        out["additionalProperties"] = False
    if "items" in out:
        out["items"] = _clean(out["items"])
    return out


def to_dust(schema: dict, nom: str) -> dict:
    """Enveloppe Dust complète, prête à coller dans Advanced › Structured Response Format."""
    return {"type": "json_schema",
            "json_schema": {"name": NOMS.get(nom, nom), "strict": True,
                            "schema": _clean(copy.deepcopy(schema))}}
