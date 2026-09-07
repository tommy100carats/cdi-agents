# -*- coding: utf-8 -*-
"""Statuts du CRM : ordre, précédence (jamais de recul), classement d'un email de recrutement.

Le modèle propose un événement ; ce module décide du statut résultant. Un doute exprimé par le
modèle bloque toute progression. « Entretien » exige une preuve (invitation d'agenda ou date et
heure confirmées), une proposition de créneau ne suffit pas.
"""
import re
from dataclasses import dataclass

ORDER = ["À contacter", "Candidature envoyée", "Entretien", "Test / Étude de cas", "Offre reçue", "Accepté"]
TERMINAL = "Refusé / Clos"
PARKED = "En veille"
ALL_STATUSES = ORDER + [TERMINAL, PARKED]

EVENT_TO_STATUS = {
    "accuse_reception": "Candidature envoyée",
    "entretien_confirme": "Entretien",
    "creneau_propose": None,          # pas de changement de statut, note + relance J+1
    "test": "Test / Étude de cas",
    "offre": "Offre reçue",
    "refus": TERMINAL,
    "relance_recruteur": None,
    "inconnu": None,
}

REJECT_FR = [
    "ne pas donner suite", "ne donnerons pas suite", "pas donner une suite favorable", "n'a pas été retenue",
    "n a pas ete retenue", "pas retenu", "malheureusement", "nous avons décidé de ne pas", "d'autres candidats",
    "plus proches des exigences", "nous ne poursuivrons pas", "ne correspond pas", "pas été sélectionné",
]
REJECT_EN = [
    "unfortunately", "not be progressing", "will not be moving forward", "not moving forward", "decided not to",
    "other candidates", "more closely match", "regret to inform", "we won't be", "won't be moving",
    "not the right fit at this time", "decided to pursue other", "not selected",
]
ACK = ["bien reçu", "avons bien reçu", "we received", "we have received", "thank you for applying",
       "thanks for applying", "will review", "merci pour votre candidature", "merci pour ta candidature",
       "application has been received", "accusé de réception"]
INTERVIEW_CONFIRMED = ["interview confirmation", "confirmation d'entretien", "you have been scheduled",
                       "is confirmed", "est confirmé", "invitation:", "calendar invite", "meet.google.com",
                       "zoom.us/j/", "teams.microsoft.com/l/meetup"]
SLOT_PROPOSED = ["book a slot", "book a time", "choose a time", "pick a time", "select a time", "calendly",
                 "réserver un créneau", "choisir un créneau", "vos disponibilités", "your availability",
                 "schedule a call", "let me know when", "quand seriez-vous disponible"]
TEST = ["case study", "étude de cas", "business case", "take-home", "assessment", "test technique", "exercice"]
OFFER = ["offer letter", "proposition d'embauche", "we'd like to offer", "we are pleased to offer",
         "job offer", "proposition de contrat"]


@dataclass
class Classification:
    event: str
    confidence: float
    needs_review: bool
    evidence: str


def _has(text: str, needles) -> str:
    for n in needles:
        if n in text:
            return n
    return ""


def classify_email(subject: str, body: str) -> Classification:
    """Classe un email de recrutement. Déterministe : lexique, pas de jugement."""
    t = f"{subject}\n{body}".lower()
    hit = _has(t, REJECT_FR + REJECT_EN)
    if hit:
        return Classification("refus", 0.95, False, hit)
    hit = _has(t, OFFER)
    if hit:
        return Classification("offre", 0.8, True, hit)
    hit = _has(t, TEST)
    if hit:
        return Classification("test", 0.8, True, hit)
    confirmed = _has(t, INTERVIEW_CONFIRMED)
    has_datetime = bool(re.search(r"\b\d{1,2}[:h]\d{2}\b", t)) and bool(
        re.search(r"\b(lundi|mardi|mercredi|jeudi|vendredi|monday|tuesday|wednesday|thursday|friday|"
                  r"\d{1,2}\s+(janvier|f[ée]vrier|mars|avril|mai|juin|juillet|ao[uû]t|septembre|octobre|"
                  r"novembre|d[ée]cembre|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\b)", t))
    if confirmed and has_datetime:
        return Classification("entretien_confirme", 0.9, False, confirmed)
    slot = _has(t, SLOT_PROPOSED)
    if slot:
        return Classification("creneau_propose", 0.85, False, slot)
    if confirmed:
        return Classification("entretien_confirme", 0.6, True, confirmed)
    ack = _has(t, ACK)
    if ack:
        return Classification("accuse_reception", 0.9, False, ack)
    return Classification("inconnu", 0.3, True, "")


def rank(status: str) -> int:
    return ORDER.index(status) if status in ORDER else -1


def advance(current: str, event: str, doubt: bool = False):
    """Statut résultant d'un événement. Retourne (statut, changé, motif)."""
    if current not in ALL_STATUSES:
        return current, False, f"statut inconnu « {current} », aucune écriture"
    if doubt:
        return current, False, "doute exprimé : progression bloquée, note seulement"
    target = EVENT_TO_STATUS.get(event)
    if event == "refus":
        if current in ("Accepté",):
            return current, False, "refus reçu sur un dossier accepté : à relire"
        return TERMINAL, current != TERMINAL, "refus"
    if target is None:
        return current, False, f"événement « {event} » ne change pas le statut"
    if current == TERMINAL:
        return current, False, "dossier clos : aucune progression sans réouverture manuelle"
    if current == PARKED:
        # une vraie interaction de recrutement réveille une fiche en veille
        return target, True, "fiche en veille réveillée par une interaction"
    if rank(target) > rank(current):
        return target, True, f"{current} → {target}"
    return current, False, f"« {target} » ne dépasse pas « {current} » : pas de recul"


def relance_after(event: str, base_date, doubt: bool = False):
    """Date de prochaine relance après un événement (None = ne pas toucher)."""
    from datetime import timedelta
    if doubt:
        return None
    delta = {"accuse_reception": 10, "entretien_confirme": 2, "creneau_propose": 1, "test": 3,
             "offre": 1, "relance_recruteur": 1}.get(event)
    return base_date + timedelta(days=delta) if delta else None
