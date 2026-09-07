# -*- coding: utf-8 -*-
"""Expérience demandée par une annonce, et sa lecture pour le profil de Tom.

Règle posée par Tom le 06/09/2026 : cible = postes demandant moins de 3 ans en opérations ;
3 à 5 ans passent aussi « au cas où » ; au-delà de 5 ans, hors cible. Aucune donnée → inconnu,
accepté et signalé (un vide n'est pas un zéro).
"""
import re

_NUM = r"(\d{1,2})"
_PATTERNS = [
    # 3-5 ans / 3 à 5 ans / 3 to 5 years
    re.compile(rf"{_NUM}\s*(?:-|–|à|to)\s*{_NUM}\s*\+?\s*(?:ans|years|yrs|year)", re.IGNORECASE),
    # 3+ ans / 3 ans minimum / minimum 3 ans / at least 3 years / 3 years of experience
    re.compile(rf"(?:minimum|min\.?|at least|au moins|plus de|more than|over)?\s*{_NUM}\s*\+?\s*(?:ans|years|yrs|year)", re.IGNORECASE),
]
_WORDS = {"junior": 1, "débutant": 0, "entry level": 0, "entry-level": 0, "graduate": 0,
          "senior": 6, "confirmé": 4, "lead": 6, "head of": 8, "director": 8, "vp ": 10}


def years_required(text: str):
    """Retourne (min, max) d'années demandées, ou (None, None) si rien n'est écrit."""
    t = text or ""
    m = _PATTERNS[0].search(t)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        return (min(lo, hi), max(lo, hi))
    candidates = []
    for m in _PATTERNS[1].finditer(t):
        n = int(m.group(1))
        if 0 <= n <= 20:
            candidates.append(n)
    if candidates:
        # plusieurs mentions : on garde la plus petite (souvent le minimum réel), sans borne haute
        lo = min(candidates)
        return (lo, lo if "+" not in t[m.start():m.end()] else None)
    return (None, None)


def band(text: str) -> dict:
    """Classe l'annonce : coeur (≤ 3 ans), stretch (3 à 5), hors (> 5), inconnu."""
    lo, hi = years_required(text)
    tl = (text or "").lower()
    if lo is None:
        for w, y in _WORDS.items():
            if w in tl:
                lo = y
                break
    if lo is None:
        return {"years_min": None, "years_max": None, "band": "inconnu", "reason": "aucune durée écrite"}
    if lo <= 3:
        b = "coeur"
    elif lo <= 5:
        b = "stretch"
    else:
        b = "hors"
    return {"years_min": lo, "years_max": hi, "band": b, "reason": f"{lo} an(s) minimum écrit(s)"}


def sourcing_decision(text: str) -> dict:
    """Décision de sourcing déterministe. « hors » est écarté avec motif ; le reste passe à Hugo."""
    b = band(text)
    b["keep"] = b["band"] in ("coeur", "stretch", "inconnu")
    return b
