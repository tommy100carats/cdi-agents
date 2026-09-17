# -*- coding: utf-8 -*-
"""Verdict déterministe à partir de la note de Hugo (calibration du 07/09/2026, règles R11 à R15).

Hugo calcule la note (A + B + C + D). Le verdict, lui, ne se discute pas : seuils fixes, plus trois
plafonds qui ne touchent jamais à la note (R7, pas de malus) mais empêchent un brief de Camille :

- R13 : titre Senior / Lead / Head / Director avec 5 ans et plus demandés → au mieux « veille » ;
- R14 : poste hors opérations (produit, ingénierie, conseil IA, data) → au mieux « veille » ;
- R15 : texte partiel → au mieux « veille » (Camille ne peut pas briefer sans l'annonce).

Un dossier déjà ouvert chez l'entreprise donne « dossier_ouvert », note calculée quand même.

Règles du 16/09/2026 (motifs des refus reçus et consignes de Tom) :
- R17 : titre Senior / Lead / Head / Director → au mieux « veille », sauf si 3 ans ou moins sont écrits ;
- R18 : administration CRM en production (Salesforce, HubSpot) exigée comme exigence centrale → au mieux « veille »
  (refus Mirakl du 15/09 après entretien, Dust du 11/09) ;
- R19 : grand groupe coté (CAC 40, SBF 120, big tech cotée type Amazon) → seuil go abaissé à 13 : Tom accepte un
  poste moins sur mesure dans un grand groupe pour monter ensuite ;
- R20 : salaire affiché (haut de fourchette) inférieur à 40 k€ → no_go.
"""
import re

SEUIL_GO = 13  # R27 (17/09/2026, consigne de Tom) : 13 et plus = CRM ; était 15
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
    """R13 + R17 : titre senior, sauf si 3 ans ou moins sont écrits."""
    if not _SENIOR_TITLE.search(title or ""):
        return False
    return years_min is None or years_min > 3


SEUIL_GO_GRAND_GROUPE = 13
SALAIRE_MIN = 40000


def verdict(note: int, *, dossier_ouvert: bool = False, titre: str = "", annees_min=None,
            texte_partiel: bool = False, grand_groupe: bool = False, crm_admin: bool = False,
            salaire_max=None, bande=None, seuil_go: int = SEUIL_GO, seuil_veille: int = SEUIL_VEILLE) -> dict:
    """Verdict et plafond éventuel. La note n'est jamais modifiée."""
    note = int(note)
    plafonds = []
    if grand_groupe:
        seuil_go = min(seuil_go, SEUIL_GO_GRAND_GROUPE)
    if senior_cap(titre, annees_min):
        plafonds.append(f"R17 : titre senior ({'durée non écrite' if annees_min is None else str(annees_min) + ' ans demandés'})")
    elif annees_min is not None and annees_min >= 5:
        # 17/09/2026 : un titre neutre qui demande 5 ans et plus n'était pas plafonné
        plafonds.append(f"R17 : {annees_min} ans demandés")
    if bande == "stretch" and not grand_groupe:
        plafonds.append("R17 : bande stretch (4 ans demandés) hors grand groupe coté")
    if crm_admin:
        plafonds.append("R18 : administration CRM en production exigée (Salesforce / HubSpot)")
    h = hors_operations(titre)
    if h:
        plafonds.append(f"R14 : poste hors opérations (« {h} » dans le titre)")
    if texte_partiel:
        plafonds.append("R15 : texte partiel, pas de brief possible")

    if salaire_max is not None and salaire_max < SALAIRE_MIN:
        return {"note": note, "verdict": "no_go", "plafonds": [f"R20 : salaire affiché {salaire_max} € < 40 k€"],
                "plafonne": True, "seuil_go": seuil_go}
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
    return {"note": note, "verdict": v, "plafonds": plafonds, "plafonne": plafonne, "seuil_go": seuil_go}
