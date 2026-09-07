# -*- coding: utf-8 -*-
"""Verdict déterministe à partir de la note de Hugo (calibration du 07/09/2026, règles R11 à R15).

Hugo calcule la note (A + B + C + D). Le verdict, lui, ne se discute pas : seuils fixes, plus trois
plafonds qui ne touchent jamais à la note (R7, pas de malus) mais empêchent un brief de Camille :

- R13 : titre Senior / Lead / Head / Director avec 5 ans et plus demandés → au mieux « veille » ;
- R14 : poste hors opérations (produit, ingénierie, conseil IA, data) → au mieux « veille » ;
- R15 : texte partiel → au mieux « veille » (Camille ne peut pas briefer sans l'annonce).

Un dossier déjà ouvert chez l'entreprise donne « dossier_ouvert », note calculée quand même.
"""
import re

SEUIL_GO = 15
SEUIL_VEILLE = 12

_SENIOR_TITLE = re.compile(r"(?<![a-zà-ÿ])(senior|lead|head of|head|director|directeur|directrice|vp|principal)(?![a-zà-ÿ])", re.IGNORECASE)

# Titres hors opérations : ce que Tom a refusé à 13/20 ou moins même en grand groupe (Bpifrance, CNAM, Thales,
# Meilleurtaux, DFM). Lu dans le TITRE seulement, jamais dans le corps.
_HORS_OPS = re.compile(
    r"product (owner|manager)|(?<![a-z])p\.?o\.?(?![a-z])|product officer|consultant|engineer|ingénieur|ingenieur|"
    r"business analyst|data (scientist|analyst|engineer)|scientist|développeur|developer|architect|"
    r"ai transformation|machine learning|\bml\b",
    re.IGNORECASE,
)


def hors_operations(title: str):
    """Renvoie le mot du titre qui place le poste hors opérations, ou None."""
    m = _HORS_OPS.search(title or "")
    return m.group(0) if m else None


def senior_cap(title: str, years_min) -> bool:
    """R13 : titre senior ET 5 ans et plus demandés."""
    return bool(_SENIOR_TITLE.search(title or "")) and years_min is not None and years_min >= 5


def verdict(note: int, *, dossier_ouvert: bool = False, titre: str = "", annees_min=None,
            texte_partiel: bool = False, seuil_go: int = SEUIL_GO, seuil_veille: int = SEUIL_VEILLE) -> dict:
    """Verdict et plafond éventuel. La note n'est jamais modifiée."""
    note = int(note)
    plafonds = []
    if senior_cap(titre, annees_min):
        plafonds.append(f"R13 : titre senior et {annees_min} ans demandés")
    h = hors_operations(titre)
    if h:
        plafonds.append(f"R14 : poste hors opérations (« {h} » dans le titre)")
    if texte_partiel:
        plafonds.append("R15 : texte partiel, pas de brief possible")

    if dossier_ouvert:
        v = "dossier_ouvert"
    elif note >= seuil_go:
        v = "go_prioritaire"
    elif note >= seuil_veille:
        v = "veille"
    else:
        v = "no_go"

    plafonne = False
    if v == "go_prioritaire" and plafonds:
        v, plafonne = "veille", True
    return {"note": note, "verdict": v, "plafonds": plafonds, "plafonne": plafonne}
