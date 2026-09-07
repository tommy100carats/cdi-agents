# -*- coding: utf-8 -*-
"""Relances : quelles candidatures relancer, dans quel ordre, avec quel message.

Règles (posées dans rules/statuts.md) :
- Candidature envoyée sans retour humain : relance à J+10, puis J+20 ; sans réponse à J+21, la
  candidature compte comme un refus dans les statistiques (elle reste ouverte dans le CRM).
- Entretien tenu : mail de remerciement à J+1 / J+2, relance à J+7 si silence.
- Créneau proposé non réservé : J+1.
- Test / étude de cas : relance à la date prévue (Prochaine relance), sinon J+3 après remise.
- Offre reçue : réponse sous 48 h.
La date « Prochaine relance » du CRM, quand elle existe, prime sur ces défauts.
"""
from datetime import date, timedelta

from .hygiene import OPEN, norm_row

DEFAULT_DELAYS = {"Candidature envoyée": 10, "Entretien": 2, "Test / Étude de cas": 3, "Offre reçue": 2}
SILENCE_AS_REJECT_DAYS = 21


def due(crm_rows, today=None):
    today = today or date.today()
    out = []
    for raw in crm_rows:
        r = norm_row(raw)
        if r["statut"] not in OPEN or r["doublon_tag"]:
            continue
        anchor = r["date_cand"] or r["cree"]
        planned = r["relance"]
        if planned is None and anchor:
            planned = anchor + timedelta(days=DEFAULT_DELAYS.get(r["statut"], 10))
        if planned is None:
            continue
        overdue = (today - planned).days
        if overdue < 0:
            continue
        silence = (today - anchor).days if anchor else None
        action = {
            "Candidature envoyée": "relance courte au recruteur (2 phrases : intérêt confirmé, disponibilité)",
            "Entretien": "mail de remerciement ou relance sur la suite du process",
            "Test / Étude de cas": "confirmer la réception du test ou demander le retour",
            "Offre reçue": "répondre à l'offre (accepter, négocier, décliner)",
        }[r["statut"]]
        out.append({
            "url": r["url"], "opportunite": r["opportunite"], "statut": r["statut"],
            "prevue": planned.isoformat(), "retard_jours": overdue,
            "silence_jours": silence, "compte_comme_refus": bool(silence and silence >= SILENCE_AS_REJECT_DAYS
                                                                    and r["statut"] == "Candidature envoyée"),
            "action": action,
            "priorite": 0 if r["statut"] == "Offre reçue" else 1 if r["statut"] == "Entretien" else 2,
        })
    return sorted(out, key=lambda x: (x["priorite"], -x["retard_jours"]))
