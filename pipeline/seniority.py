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
# Mots de niveau, lus dans le TITRE seulement (jamais dans le corps : « leadership », « senior team »
# y apparaissent sans rien dire du poste). Incident du 07/09/2026 : un « Junior Sales Operations Analyst »
# était classé « hors » parce que le corps contenait « lead ». Ordre : les mots juniors gagnent.
_WORDS = [("junior", 1), ("débutant", 0), ("entry level", 0), ("entry-level", 0), ("graduate", 0),
          ("associate", 1), ("head of", 8), ("director", 8), ("directeur", 8), ("directrice", 8), ("vp", 10),
          ("senior", 5), ("confirmé", 4), ("confirmée", 4), ("lead", 6)]


# Une durée ne compte que si elle parle d'expérience. Incident du 07/09/2026 : « vos données peuvent être
# conservées 2 ans » (politique RGPD en pied d'annonce) et « en 6 ans d'existence » étaient lus comme des
# années d'expérience demandées.
# Incident du 10/09/2026 : « Your data is kept for up to 2 years » (Qonto) lu comme 2 ans d'expérience.
_EXP_CONTEXT = re.compile(r"exp[ée]rience|experience|années? d'|years? (?:of|in)|yrs|minimum|at least|au moins|\+", re.IGNORECASE)
_NOT_EXP = re.compile(r"conserv|retain|retention|kept|keep (?:your|them)|stored|stock[ée]|gard[ée]es?|up to|jusqu'à|existence|fond[ée]e|founded|il y a|ago|depuis|since|garantie|warranty|contrat de|cdd de|mission de|tous les|every|per year|par an\b", re.IGNORECASE)


def _negated(text, start, end):
    near = text[max(0, start - 20): end + 30]
    return bool(_NOT_EXP.search(near))


def _in_experience_context(text, start, end):
    window = text[max(0, start - 70): end + 40]
    return bool(_EXP_CONTEXT.search(window)) and not _negated(text, start, end)


def years_required(text: str):
    """Retourne (min, max) d'années demandées, ou (None, None) si rien n'est écrit."""
    t = text or ""
    for m in _PATTERNS[0].finditer(t):
        # une fourchette « 3 à 5 ans » parle presque toujours d'expérience ; on n'exclut que les faux amis
        if not _negated(t, m.start(), m.end()):
            lo, hi = int(m.group(1)), int(m.group(2))
            return (min(lo, hi), max(lo, hi))
    candidates = []
    for m in _PATTERNS[1].finditer(t):
        n = int(m.group(1))
        if 0 <= n <= 20 and _in_experience_context(t, m.start(), m.end()):
            candidates.append((n, "+" in t[m.start():m.end()] or bool(re.search(r"minimum|at least|au moins|plus de|more than|over", t[max(0, m.start() - 15):m.end()], re.I))))
    if candidates:
        # plusieurs mentions : on garde la plus petite (souvent le minimum réel) ; « 5+ » ou « au moins 5 » = sans borne haute
        lo, plus = min(candidates)
        return (lo, None if plus else lo)
    return (None, None)


def title_level(title: str):
    """Niveau implicite d'un TITRE (mot entier), ou None. Jamais appliqué au corps de l'annonce."""
    tl = (title or "").lower()
    for w, y in _WORDS:
        if re.search(r"(?<![a-zà-ÿ])" + re.escape(w) + r"(?![a-zà-ÿ])", tl):
            return y, w
    return None


def band(text: str, title: str = "") -> dict:
    """Classe l'annonce : coeur (≤ 3 ans), stretch (3 à 5), hors (> 5), inconnu.

    Les années écrites dans le texte priment ; à défaut, un mot de niveau dans le titre ; sinon inconnu.
    """
    lo, hi = years_required(text)
    reason = None
    if lo is None and title:
        tv = title_level(title)
        if tv:
            lo, reason = tv[0], f"aucune durée écrite ; « {tv[1]} » dans le titre"
    if lo is None:
        return {"years_min": None, "years_max": None, "band": "inconnu", "reason": "aucune durée écrite"}
    if lo <= 3:
        b = "coeur"
    elif lo <= 5:
        b = "stretch"
    else:
        b = "hors"
    return {"years_min": lo, "years_max": hi, "band": b, "reason": reason or f"{lo} an(s) minimum écrit(s)"}


def sourcing_decision(text: str, title: str = "") -> dict:
    """Décision de sourcing déterministe. « hors » est écarté avec motif ; le reste passe à Hugo."""
    b = band(text, title)
    b["keep"] = b["band"] in ("coeur", "stretch", "inconnu")
    return b
