# -*- coding: utf-8 -*-
"""Anti-doublon déterministe sur clé métier, entre nouvelles offres et base existante.

Entrées : les lignes existantes du CRM (export JSON) et de l'Inbox, et les candidates du jour.
Sorties : pour chaque candidate, `decision` = nouvelle | doublon_crm | doublon_inbox | doublon_lot,
avec la ligne existante pointée. Aucune candidate n'est perdue : un doublon est une ligne Inbox
« Doublon » avec le lien vers l'original, pas une suppression.
"""
from .keys import business_key, key_from_opportunite


def _clean_key(k):
    """Clé lue dans un export Notion : le mode view échappe « | » en « \\| » (incident du 17/09/2026 :
    aucun doublon Inbox détecté). On dé-échappe et on retire les espaces."""
    return str(k or "").replace("\\|", "|").strip()


def index_existing(crm_rows, inbox_rows=None):
    """Construit {clé: {source, url, statut, titre}} à partir des exports Notion."""
    idx = {}
    for r in crm_rows or []:
        k = _clean_key(r.get("Clé") or key_from_opportunite(r.get("Opportunité", "")))
        if k and k not in idx:  # la première (la plus ancienne si trié) fait foi
            idx[k] = {"source": "crm", "url": r.get("url"), "statut": r.get("Statut"),
                      "titre": r.get("Opportunité"), "doublon_tag": str(r.get("Opportunité", "")).startswith("🗑️")}
    for r in inbox_rows or []:
        k = _clean_key(r.get("cle") or r.get("Clé"))
        if k and k not in idx:
            idx[k] = {"source": "inbox", "url": r.get("url"), "statut": r.get("Étape") or r.get("etape"),
                      "titre": r.get("Titre") or r.get("titre"), "doublon_tag": False}
    return idx


def company_lines(crm_rows, company_norm):
    """Nombre de lignes existantes pour cet employeur (pour l'avertissement « ne pas candidater en parallèle »)."""
    from .keys import normalize_company, split_opportunite
    n = 0
    for r in crm_rows or []:
        _, ent = split_opportunite(r.get("Opportunité", ""))
        if normalize_company(ent) == company_norm and not str(r.get("Opportunité", "")).startswith("🗑️"):
            n += 1
    return n


def decide(candidates, crm_rows, inbox_rows=None):
    """Ajoute à chaque candidate : cle, decision, existant (dict|None), lignes_employeur."""
    from .keys import normalize_company
    idx = index_existing(crm_rows, inbox_rows)
    seen_in_batch = {}
    out = []
    for c in candidates:
        k = _clean_key(c.get("cle")) or business_key(c.get("entreprise", ""), c.get("titre", ""))
        c = dict(c, cle=k)
        if not k:
            c.update(decision="cle_invalide", existant=None)
        elif k in idx:
            c.update(decision=f"doublon_{idx[k]['source']}", existant=idx[k])
        elif k in seen_in_batch:
            c.update(decision="doublon_lot", existant={"source": "lot", "titre": seen_in_batch[k]})
        else:
            seen_in_batch[k] = c.get("titre")
            c.update(decision="nouvelle", existant=None)
        c["lignes_employeur"] = company_lines(crm_rows, normalize_company(c.get("entreprise", "")))
        out.append(c)
    return out


def find_duplicates(crm_rows):
    """Groupes de lignes CRM partageant une clé (hors lignes déjà taguées 🗑️)."""
    groups = {}
    for r in crm_rows or []:
        title = str(r.get("Opportunité", ""))
        if title.startswith("🗑️"):
            continue
        k = _clean_key(r.get("Clé") or key_from_opportunite(title))
        if k:
            groups.setdefault(k, []).append(r)
    return {k: v for k, v in groups.items() if len(v) > 1}
