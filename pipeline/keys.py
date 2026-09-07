# -*- coding: utf-8 -*-
"""Clé métier d'une offre : entreprise normalisée + intitulé normalisé.

Pourquoi : l'anti-doublon v1 travaillait sur l'URL. La même offre republiée sur un autre site
produit une autre URL, donc un doublon (13 sur 199 le 02/09/2026). Une clé métier est calculée
ici, par du code, jamais par le modèle. Deux offres ont la même clé si et seulement si elles
décrivent le même poste chez le même employeur.
"""
import re
import unicodedata

# Suffixes juridiques et mots vides côté entreprise
_COMPANY_NOISE = re.compile(
    r"\b(sas|sasu|sa|sarl|eurl|inc|ltd|llc|gmbh|bv|plc|group|groupe|company|co|france|europe|"
    r"paris|holding|international)\b",
    re.IGNORECASE,
)
# Marqueurs de genre et de contrat côté intitulé
_TITLE_NOISE = re.compile(
    r"\(?\b(h\s*/\s*f\s*/?\s*x?|f\s*/\s*h|m\s*/\s*f|f\s*/\s*m\s*/?\s*x?|w\s*/\s*m|m\s*/\s*w|h/f/d|m/f/d)\b\)?"
    r"|\b(cdi|cdd|full[- ]?time|temps plein|permanent|stage|internship|alternance)\b",
    re.IGNORECASE,
)

# Alias d'employeurs : plusieurs marques, un seul employeur (à enrichir dans rules/sources.md)
COMPANY_ALIASES = {
    "aviv": "seloger",
    "aviv group": "seloger",
    "seloger aviv": "seloger",
    "gympass": "wellhub",
    "1000mercis": "numberly",
    "clutch": "primo",
    "hanesbrands": "dim",
}


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def _clean(s: str) -> str:
    s = strip_accents(s or "").lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def normalize_company(name: str) -> str:
    # « Numberly (groupe 1000mercis) » : la parenthèse est une précision, pas l'employeur
    name = re.sub(r"\([^)]*\)", " ", name or "")
    s = _clean(name)
    s = _COMPANY_NOISE.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return COMPANY_ALIASES.get(s, s)


def normalize_title(title: str) -> str:
    s = _TITLE_NOISE.sub(" ", title or "")
    s = _clean(s)
    # « senior » et « junior » restent : ce ne sont pas les mêmes postes
    return s


def business_key(company: str, title: str) -> str:
    """Clé stable : `entreprise|intitulé`. Vide si l'un des deux manque (jamais de faux positif)."""
    c, t = normalize_company(company), normalize_title(title)
    if not c or not t:
        return ""
    return f"{c}|{t}"


def split_opportunite(opportunite: str):
    """« Poste — Entreprise » (format du CRM) → (poste, entreprise). Tolère le tiret court."""
    if not opportunite:
        return "", ""
    s = re.sub(r"^\W*doublon\W*", "", opportunite, flags=re.IGNORECASE)
    for sep in (" — ", " – ", " - "):
        if sep in s:
            poste, entreprise = s.rsplit(sep, 1)
            return poste.strip(), entreprise.strip()
    return s.strip(), ""


def key_from_opportunite(opportunite: str) -> str:
    poste, entreprise = split_opportunite(opportunite)
    return business_key(entreprise, poste)
