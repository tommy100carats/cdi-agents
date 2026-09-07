# -*- coding: utf-8 -*-
"""Exclusions fermes lisibles par le code (rules/criteres.md § 1).

Incident du 07/09/2026 : « AI Transformation Senior » (Meilleurtaux) exigeait « Bac +5 École d'Ingénieurs ou
Master Informatique » et a été noté au lieu d'être écarté. Léa appelle `pipeline.cli exclusions` sur chaque
texte avant de retenir l'offre. Une exclusion est une phrase citée, jamais une impression.
"""
import re

_DEGREE = re.compile(
    r"[^.\n]{0,80}(dipl[ôo]me d'ing[ée]nieur|[ée]cole d'ing[ée]nieurs?|engineering degree|ing[ée]nieur de formation|"
    r"master (?:en )?informatique|computer science degree|degree in computer science)[^.\n]{0,80}",
    re.IGNORECASE,
)
_ALTERNATIVE = re.compile(r"commerce|business school|management|universit|équivalent|equivalent|ou (?:master|bac)", re.IGNORECASE)
_REQUIRED = re.compile(r"exig|requis|obligatoire|required|must|impératif|imperatif|indispensable|de formation|bac\s*\+\s*5|profil", re.IGNORECASE)

_CODE = re.compile(
    r"[^.\n]{0,80}(?:langchain|langgraph|ci/?cd|pipelines? de donn[ée]es|data pipelines?|code de production|production code|"
    r"software engineer|ml engineer|data scientist|machine learning engineer)[^.\n]{0,80}",
    re.IGNORECASE,
)
_CODE_REQUIRED = re.compile(r"ma[îi]trise|exig|requis|required|must|solide|strong|expert|hands-on|quotidien|daily", re.IGNORECASE)


def engineer_degree_required(text: str):
    """Phrase qui exige un diplôme d'ingénieur ou d'informatique sans alternative commerce, sinon None."""
    for m in _DEGREE.finditer(text or ""):
        phrase = m.group(0).strip()
        if _ALTERNATIVE.search(phrase) and not re.search(r"informatique|computer science", phrase, re.I):
            continue
        if _ALTERNATIVE.search(phrase) and re.search(r"commerce|business", phrase, re.I):
            continue
        if _REQUIRED.search(phrase):
            return phrase
    return None


def code_required(text: str):
    """Phrase qui fait du code ou des pipelines de données le coeur du poste, sinon None."""
    for m in _CODE.finditer(text or ""):
        phrase = m.group(0).strip()
        if _CODE_REQUIRED.search(phrase):
            return phrase
    return None


def check(text: str) -> dict:
    """Décision déterministe : {"exclue": bool, "motifs": [phrases citées]}."""
    motifs = []
    d = engineer_degree_required(text)
    if d:
        motifs.append("diplôme d'ingénieur ou d'informatique exigé : « " + d + " »")
    c = code_required(text)
    if c:
        motifs.append("code ou pipelines de données au coeur du poste : « " + c + " »")
    return {"exclue": bool(motifs), "motifs": motifs}
