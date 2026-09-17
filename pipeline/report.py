# -*- coding: utf-8 -*-
"""Rapport pipeline : HTML (corps de l'email) et PDF (pièce jointe ou Drive), à partir d'un export.

Deux modes :
- « soir » : l'état des candidatures comme un pipeline commercial (dossiers ouverts par étape,
  prochaine action, relances dues, activité du jour, hygiène). Envoyé chaque soir par Noé.
- « pipeline » : la vue complète du mardi et du vendredi (entonnoir depuis le sourcing, taux de
  conversion, offres à contacter par famille, veille, semaine écoulée).
Le générateur ne décide rien : il met en forme ce que hygiene.py et relances.py ont calculé.
"""
import html
from collections import Counter
from datetime import date, timedelta

from . import hygiene, relances
from .precedence import ORDER, PARKED, TERMINAL

NAVY, GOLD, GREY, LINE = "#16243d", "#c6a24a", "#6b7280", "#e3e6eb"

CSS = f"""
@page {{ size: A4; margin: 14mm; }}
body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10pt; color: #222; margin: 0; }}
h1 {{ color: {NAVY}; font-size: 18pt; margin: 0 0 2mm 0; }}
h2 {{ color: {NAVY}; font-size: 12pt; margin: 6mm 0 2mm 0; border-bottom: 1px solid {LINE}; padding-bottom: 1mm; }}
.kicker {{ color: {GOLD}; font-size: 8pt; letter-spacing: 1.5pt; text-transform: uppercase; font-weight: bold; }}
.sub {{ color: {GREY}; font-size: 9pt; margin-bottom: 4mm; }}
table {{ border-collapse: collapse; width: 100%; margin: 2mm 0; }}
th {{ text-align: left; font-size: 8pt; color: {GOLD}; text-transform: uppercase; letter-spacing: 1pt; padding: 1.5mm 2mm; border-bottom: 1px solid {LINE}; }}
td {{ padding: 1.5mm 2mm; border-bottom: 1px solid #f0f1f4; vertical-align: top; }}
.stat {{ display: inline-block; width: 22%; margin-right: 2%; background: #f4f5f8; border-radius: 3mm; padding: 3mm; }}
.stat b {{ font-size: 20pt; color: {NAVY}; display: block; }}
.stat span {{ color: {GREY}; font-size: 8pt; }}
.pill {{ display: inline-block; padding: 0.5mm 2mm; border-radius: 3mm; font-size: 8pt; font-weight: bold; }}
.late {{ background: #f6e2de; color: #b3412f; }} .ok {{ background: #e1f1ea; color: #2e7d5b; }} .warn {{ background: #f3ead3; color: #7a5e1e; }}
.muted {{ color: {GREY}; font-size: 8.5pt; }}
"""


def _esc(s):
    return html.escape("" if s is None else str(s))


def _funnel(rows):
    c = Counter(r["statut"] for r in rows if not r["doublon_tag"])
    return [(s, c.get(s, 0)) for s in ORDER + [TERMINAL, PARKED]]


def build(crm_rows, mode="soir", today=None, inbox_rows=None, runs_rows=None, title=None):
    today = today or date.today()
    rows = [hygiene.norm_row(r) for r in crm_rows]
    hyg = hygiene.run(crm_rows, today=today, inbox_rows=inbox_rows, runs_rows=runs_rows)
    dues = relances.due(crm_rows, today=today)
    open_rows = sorted([r for r in rows if r["statut"] in hygiene.OPEN and not r["doublon_tag"]],
                       key=lambda r: (ORDER.index(r["statut"]) * -1, r["date_cand"] or date.min))
    week_ago = today - timedelta(days=7)
    created_week = [r for r in rows if r["cree"] and r["cree"] >= week_ago and not r["doublon_tag"]]
    applied_week = [r for r in rows if r["date_cand"] and r["date_cand"] >= week_ago]
    fun = _funnel(rows)
    n_sent = sum(v for s, v in fun if s in ("Candidature envoyée", "Point mort", "Entretien", "Test / Étude de cas", "Offre reçue", "Accepté"))
    n_int = sum(v for s, v in fun if s in ("Entretien", "Test / Étude de cas", "Offre reçue", "Accepté"))

    title = title or ("État des candidatures" if mode == "soir" else "Pipeline d'offres")
    parts = [f"<div class='kicker'>Recherche CDI · {'point du soir' if mode == 'soir' else 'point du ' + ('mardi' if today.weekday() == 1 else 'vendredi' if today.weekday() == 4 else today.strftime('%A'))}</div>",
             f"<h1>{_esc(title)}</h1>",
             f"<div class='sub'>{today.strftime('%d/%m/%Y')} · {hyg['resume']['lignes_actives']} opportunités actives · généré par pipeline/report.py à partir de l'export Notion</div>"]

    parts.append("<div>")
    for v, l in [(hyg["resume"]["dossiers_ouverts"], "dossiers ouverts"), (len(dues), "relances dues"),
                 (n_int, "entretiens ou plus"), (f"{(100 * n_int / n_sent):.0f} %" if n_sent else "n/a", "candidature → entretien")]:
        parts.append(f"<div class='stat'><b>{_esc(v)}</b><span>{l}</span></div>")
    parts.append("</div>")

    parts.append("<h2>Dossiers ouverts, par étape</h2><table><tr><th>Étape</th><th>Opportunité</th><th>Candidature</th><th>Prochaine action</th><th>Âge</th></tr>")
    due_by_url = {d["url"]: d for d in dues}
    for r in open_rows:
        d = due_by_url.get(r["url"])
        age = (today - (r["date_cand"] or r["cree"])).days if (r["date_cand"] or r["cree"]) else None
        if d:
            act = f"<span class='pill late'>relance J+{d['retard_jours']}</span> {_esc(d['action'])}"
        elif r["relance"]:
            act = f"<span class='pill ok'>prévue le {r['relance'].strftime('%d/%m')}</span>"
        else:
            act = "<span class='pill warn'>relance à poser</span>"
        parts.append(f"<tr><td>{_esc(r['statut'])}</td><td><b>{_esc(r['opportunite'])}</b></td>"
                     f"<td>{r['date_cand'].strftime('%d/%m') if r['date_cand'] else 'n/c'}</td><td>{act}</td><td>{age if age is not None else 'n/c'} j</td></tr>")
    if not open_rows:
        parts.append("<tr><td colspan='5' class='muted'>Aucun dossier ouvert.</td></tr>")
    parts.append("</table>")

    if dues:
        parts.append("<h2>À relancer, par priorité</h2><table><tr><th>Opportunité</th><th>Statut</th><th>Prévue</th><th>Retard</th><th>Silence</th><th>Action</th></tr>")
        for d in dues:
            flag = " <span class='pill late'>compte comme refus</span>" if d["compte_comme_refus"] else ""
            parts.append(f"<tr><td><b>{_esc(d['opportunite'])}</b></td><td>{_esc(d['statut'])}</td><td>{d['prevue'][5:]}</td>"
                         f"<td>{d['retard_jours']} j</td><td>{d['silence_jours'] if d['silence_jours'] is not None else 'n/c'} j{flag}</td><td>{_esc(d['action'])}</td></tr>")
        parts.append("</table>")

    if mode == "pipeline":
        parts.append("<h2>Entonnoir</h2><table><tr><th>Statut</th><th>Lignes</th></tr>")
        for s, v in fun:
            parts.append(f"<tr><td>{_esc(s)}</td><td>{v}</td></tr>")
        parts.append("</table>")
        to_contact = sorted([r for r in rows if r["statut"] == "À contacter" and not r["doublon_tag"] and (r["score"] or 0) >= 15],
                            key=lambda r: (-(r["score"] or 0), r["cree"] or date.min))
        parts.append("<h2>À contacter, note ≥ 15, par famille</h2><table><tr><th>Famille</th><th>Opportunité</th><th>Note</th><th>Publiée</th><th>Âge</th></tr>")
        for r in sorted(to_contact, key=lambda r: (["AI & Ops Automation", "RevOps", "Sales Ops", "Commercial (SDR/AE)", "Autre"].index(r["role"]) if r["role"] in ["AI & Ops Automation", "RevOps", "Sales Ops", "Commercial (SDR/AE)", "Autre"] else 9, -(r["score"] or 0))):
            age = (today - r["cree"]).days if r["cree"] else None
            parts.append(f"<tr><td>{_esc(r['role'])}</td><td><b>{_esc(r['opportunite'])}</b></td><td>{r['score']}</td>"
                         f"<td>{r['date_pub'].strftime('%d/%m') if r['date_pub'] else 'n/c'}</td><td>{age if age is not None else 'n/c'} j</td></tr>")
        parts.append("</table>")
        if inbox_rows is not None:
            c = Counter((r.get("Étape") or r.get("etape") or "?") for r in inbox_rows)
            parts.append("<h2>Inbox (chaîne du matin), par étape</h2><table><tr><th>Étape</th><th>Lignes</th></tr>")
            for k, v in sorted(c.items()):
                parts.append(f"<tr><td>{_esc(k)}</td><td>{v}</td></tr>")
            parts.append("</table>")

    parts.append("<h2>Semaine écoulée</h2>")
    parts.append(f"<p>{len(created_week)} opportunités créées, {len(applied_week)} candidatures envoyées, "
                 f"{sum(1 for r in rows if r['statut'] == TERMINAL and r['cree'] and r['cree'] >= week_ago)} clôtures sur des fiches récentes.</p>")

    pr = hyg["resume"]["problemes"]
    parts.append("<h2>Hygiène de la base</h2>")
    parts.append(f"<p>{pr.get('bloquant', 0)} bloquant, {pr.get('majeur', 0)} majeur, {pr.get('action', 0)} action, {pr.get('mineur', 0)} mineur. "
                 f"Codes : {', '.join(f'{k} ×{v}' for k, v in sorted(hyg['resume']['par_code'].items()))}</p>")
    majors = [p for p in hyg["problemes"] if p["gravite"] in ("bloquant", "majeur")][:15]
    if majors:
        parts.append("<table><tr><th>Gravité</th><th>Ligne</th><th>Problème</th><th>Correction</th></tr>")
        for p in majors:
            parts.append(f"<tr><td>{p['gravite']}</td><td>{_esc(p['ligne'])}</td><td>{_esc(p['message'])}</td><td>{_esc(p['correction'])}</td></tr>")
        parts.append("</table>")
    parts.append("<p class='muted'>Chiffres calculés par du code sur l'export du jour. Un vide est affiché n/c, jamais estimé.</p>")

    body = "\n".join(parts)
    html_doc = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    return {"html": html_doc, "hygiene": hyg, "relances": dues, "stats": {"ouverts": hyg["resume"]["dossiers_ouverts"],
            "relances_dues": len(dues), "entretiens_plus": n_int, "envoyees_total": n_sent}}


def write_pdf(html_doc, out_path):
    try:
        from weasyprint import HTML
    except ImportError:
        return None
    HTML(string=html_doc).write_pdf(out_path)
    return out_path
