# -*- coding: utf-8 -*-
"""Vérification qu'une offre est encore active, par du code.

Trois niveaux : (1) API d'ATS (Ashby, Greenhouse, Lever) : la réponse est structurée, la preuve est
forte ; (2) page HTML lisible : 404/410 ou formule « n'est plus disponible » ; (3) pages illisibles
(LinkedIn, Welcome to the Jungle, Indeed) : impossible à vérifier, résultat None, jamais « active ».

`fetch` est injectable pour les tests : (url) -> (status_code, text).
"""
import json
import re
from urllib.parse import urlparse

DEAD_PATTERNS = [
    "n'est plus disponible", "n’est plus disponible", "no longer available", "no longer accepting",
    "job has been closed", "this job is closed", "position has been filled", "cette offre a expiré",
    "offre expirée", "job not found", "this posting is no longer", "cette annonce n'est plus",
    "the job you are looking for is no longer", "l'offre que vous recherchez n'existe plus",
]
UNVERIFIABLE_HOSTS = ("linkedin.com", "welcometothejungle.com", "indeed.com", "indeed.fr", "glassdoor.")

ASHBY = re.compile(r"jobs\.ashbyhq\.com/([^/]+)/([0-9a-f-]{36})")
GREENHOUSE = re.compile(r"(?:job-boards|boards)(?:\.eu)?\.greenhouse\.io/([^/]+)/jobs/(\d+)")
LEVER = re.compile(r"jobs\.lever\.co/([^/]+)/([0-9a-f-]{36})")


def _default_fetch(url, timeout=12):
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (cdi-agents link-check)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(400_000).decode("utf-8", "ignore")
    except Exception as e:  # HTTPError a un code, le reste non
        code = getattr(e, "code", 0)
        return code or 0, ""


def check(url: str, fetch=None, today=None) -> dict:
    """Retourne {url, active: True|False|None, method, evidence}."""
    fetch = fetch or _default_fetch
    if not url:
        return {"url": url, "active": None, "method": "none", "evidence": "lien absent"}
    host = urlparse(url).netloc.lower()

    m = ASHBY.search(url)
    if m:
        slug, jid = m.groups()
        code, body = fetch(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
        return _api_result(url, "ashby", code, body, jid)
    m = GREENHOUSE.search(url)
    if m:
        slug, jid = m.groups()
        code, body = fetch(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
        return _api_result(url, "greenhouse", code, body, jid)
    m = LEVER.search(url)
    if m:
        slug, jid = m.groups()
        code, body = fetch(f"https://api.lever.co/v0/postings/{slug}?mode=json")
        return _api_result(url, "lever", code, body, jid)

    if any(h in host for h in UNVERIFIABLE_HOSTS):
        return {"url": url, "active": None, "method": "unverifiable",
                "evidence": f"{host} : page authentifiée ou rendue en JavaScript, non vérifiable par du code"}

    code, body = fetch(url)
    if code in (404, 410):
        return {"url": url, "active": False, "method": "http", "evidence": f"HTTP {code}"}
    if code == 0:
        return {"url": url, "active": None, "method": "http", "evidence": "page injoignable (timeout ou erreur réseau)"}
    low = (body or "").lower()
    for p in DEAD_PATTERNS:
        if p in low:
            return {"url": url, "active": False, "method": "http", "evidence": f"motif « {p} » dans la page"}
    if code >= 400:
        return {"url": url, "active": None, "method": "http", "evidence": f"HTTP {code}"}
    if len(low) < 500:
        return {"url": url, "active": None, "method": "http", "evidence": "page quasi vide (rendu JavaScript ?)"}
    return {"url": url, "active": True, "method": "http", "evidence": f"HTTP {code}, aucun motif de fermeture"}


def _api_result(url, ats, code, body, jid):
    if code != 200 or not body:
        return {"url": url, "active": None, "method": ats, "evidence": f"API {ats} indisponible (HTTP {code})"}
    try:
        data = json.loads(body)
    except ValueError:
        return {"url": url, "active": None, "method": ats, "evidence": f"API {ats} : réponse illisible"}
    ids = set()
    if ats == "ashby":
        ids = {str(j.get("id")) for j in data.get("jobs", [])}
    elif ats == "greenhouse":
        ids = {str(j.get("id")) for j in data.get("jobs", [])}
    elif ats == "lever":
        ids = {str(j.get("id")) for j in (data if isinstance(data, list) else [])}
    active = str(jid) in ids
    return {"url": url, "active": active, "method": ats,
            "evidence": f"id {'présent' if active else 'absent'} dans le job board {ats} ({len(ids)} offres)"}


def check_many(urls, fetch=None):
    return [check(u, fetch=fetch) for u in urls]
