# -*- coding: utf-8 -*-
"""Verdict déterministe à partir de la note de Hugo (calibration du 07/09/2026, règles R11 à R15).

Hugo calcule la note (A + B + C + D). Le verdict, lui, ne se discute pas : seuils fixes, plus trois
plafonds qui ne touchent jamais à la note (R7, pas de malus) mais empêchent un brief de Camille :

- R13 : titre Senior / Lead / Head / Director avec 5 ans et plus demandés → au mieux « veille » ;
- R14 : poste hors opérations (produit, ingénierie, conseil IA, data) → au mieux « veille » ;
- R15 : texte partiel → au mieux « veille » (Camille ne peut pas briefer sans l'annonce).

Un dossier déjà ouvert chez l'entreprise donne « dossier_ouvert », note calculée quand même.

Règles du 16/09/2026 :
- R17 : titre Senior / Lead / Head / Director → au mieux « veille », sauf si 3 ans ou moins sont écrits ;
- R18 : administration CRM en production (Salesforce, HubSpot) exigée comme exigence centrale → au mieux « veille » ;
- R19 : grand groupe coté (CAC 40, SBF 120, grande entreprise cotée) → seuil go abaissé à 13 ;
- R20 : salaire affiché (haut de fourchette) inférieur au seuil personnel → no_go. Le seuil n'est pas dans ce dépôt
  public : il est lu dans la base Notion « Paramètres système » (paramètre « Salaire minimum ») et passé par
  `--salaire-min`, ou par la variable d'environnement CDI_SALAIRE_MIN. Sans seuil, R20 ne s'applique pas.
"""
import os
import re

SEUIL_GO = 13  # R27 (17/09/2026, consigne de Tom) : 13 et plus = CRM ; était 15
SEUIL_VEILLE = 12

_SENIOR_TITLE = re.compile(r"(?<![a-zà-ÿ])(senior|lead|head of|head|director|directeur|directrice|vp|principal)(?![a-zà-ÿ])", re.IGNORECASE)

# Titres hors opérations : refusés par Tom à 13/20 ou moins même en grand groupe lors de la calibration du 07/09.
# Lu dans le TITRE seulement, jamais dans le corps.
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


def _salaire_min_env():
    v = os.environ.get("CDI_SALAIRE_MIN", "").strip()
    return int(v) if v.isdigit() else None


def verdict(note: int, *, dossier_ouvert: bool = False, titre: str = "", annees_min=None,
            texte_partiel: bool = False, grand_groupe: bool = False, crm_admin: bool = False,
            salaire_max=None, salaire_min=None, bande=None, seuil_go: int = SEUIL_GO, seuil_veille: int = SEUIL_VEILLE) -> dict:
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

    seuil_salaire = salaire_min if salaire_min is not None else _salaire_min_env()
    if salaire_max is not None and seuil_salaire is not None and salaire_max < seuil_salaire:
        return {"note": note, "verdict": "no_go", "plafonds": ["R20 : salaire affiché sous le seuil (Paramètres)"],
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
