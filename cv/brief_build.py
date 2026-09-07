#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brief_build.py : rend un ou plusieurs briefs (schemas/brief.json) en PDF, cadre fixe.

    python3 cv/brief_build.py briefs.json [--out-dir out/]

Sections, toujours dans cet ordre : en-tête, fiche de poste, entreprise, actualités, fit, sources.
Le contenu vient de Camille ; le cadre vient d'ici et ne change jamais.
"""
import html
import json
import os
import sys
from datetime import date

NAVY, GOLD, GREY, LINE = "#16243d", "#c6a24a", "#6b7280", "#e3e6eb"
CSS = f"""
@page {{ size: A4; margin: 16mm; }}
body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10pt; color: #222; }}
.kicker {{ color: {GOLD}; font-size: 8pt; letter-spacing: 1.5pt; text-transform: uppercase; font-weight: bold; }}
h1 {{ color: {NAVY}; font-size: 18pt; margin: 0 0 1mm 0; }}
.sub {{ color: {GREY}; font-size: 9pt; margin-bottom: 5mm; }}
h2 {{ color: {NAVY}; font-size: 12pt; margin: 6mm 0 2mm 0; border-bottom: 1px solid {LINE}; padding-bottom: 1mm; }}
ul {{ margin: 1mm 0 0 4mm; padding: 0; }} li {{ margin-bottom: 1mm; }}
.grid td {{ padding: 1mm 3mm 1mm 0; vertical-align: top; }} .grid td:first-child {{ color: {GREY}; width: 34mm; }}
.fit {{ background: #f4f5f8; border-radius: 3mm; padding: 3mm 4mm; }}
.muted {{ color: {GREY}; font-size: 8.5pt; }}
.score {{ display: inline-block; background: {NAVY}; color: #fff; border-radius: 3mm; padding: 1mm 3mm; font-weight: bold; }}
"""


def esc(s):
    return html.escape("" if s is None else str(s))


def render_one(b, score=None):
    score_html = f"<span class='score'>{esc(score)}/20</span> · " if score is not None else ""
    parts = [f"<div class='kicker'>Brief entreprise · {date.today().strftime('%d/%m/%Y')}</div>",
             f"<h1>{esc(b['poste'])} — {esc(b['entreprise'])}</h1>",
             f"<div class='sub'>{score_html}cadre fixe : fiche de poste, entreprise, actualités, fit, sources</div>"]
    parts.append("<h2>1. La fiche de poste</h2>")
    if b.get("missions_verbatim"):
        parts.append("<ul>" + "".join(f"<li>{esc(m)}</li>" for m in b["missions_verbatim"][:6]) + "</ul>")
    parts.append("<table class='grid'>")
    parts.append(f"<tr><td>Stack citée</td><td>{esc(', '.join(b.get('stack_verbatim') or [])) or 'n/c'}</td></tr>")
    parts.append(f"<tr><td>Niveau de code attendu</td><td>{esc(b.get('niveau_code_verbatim')) or 'n/c'}</td></tr>")
    parts.append(f"<tr><td>Recruteur / manager</td><td>{esc(b.get('recruteur')) or 'n/c'}</td></tr>")
    parts.append("</table>")
    parts.append("<h2>2. L'entreprise</h2><table class='grid'>")
    parts.append(f"<tr><td>Activité</td><td>{esc(b.get('activite'))}</td></tr>")
    parts.append(f"<tr><td>Effectif</td><td>{esc(b.get('effectif')) or 'n/c'}</td></tr>")
    parts.append(f"<tr><td>Levée ou CA connus</td><td>{esc(b.get('levee_ou_ca')) or 'n/c'}</td></tr>")
    parts.append(f"<tr><td>Grand groupe</td><td>{'oui' if b.get('grand_groupe') else 'non'}</td></tr>")
    parts.append(f"<tr><td>Note Glassdoor</td><td>{esc(b.get('note_glassdoor')) if b.get('note_glassdoor') is not None else 'n/c'}</td></tr>")
    parts.append("</table>")
    parts.append("<h2>3. Les dernières actualités</h2>")
    acts = b.get("actualites") or []
    if acts:
        parts.append("<ul>" + "".join(f"<li><b>{esc(a.get('date')) or 'date n/c'}</b> · {esc(a['titre'])} <span class='muted'>({esc(a['source'])})</span></li>" for a in acts) + "</ul>")
    else:
        parts.append("<p class='muted'>Aucune actualité sourcée trouvée.</p>")
    parts.append("<h2>4. Le fit</h2>")
    parts.append(f"<div class='fit'>{esc(b.get('fit'))}</div>")
    parts.append("<h2>5. Sources</h2><ul>" + "".join(f"<li class='muted'>{esc(s)}</li>" for s in b.get("sources", [])) + "</ul>")
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"


def main(argv):
    src = argv[1]
    out_dir = argv[argv.index("--out-dir") + 1] if "--out-dir" in argv else "."
    os.makedirs(out_dir, exist_ok=True)
    briefs = json.load(open(src, encoding="utf-8"))
    briefs = briefs if isinstance(briefs, list) else [briefs]
    try:
        from weasyprint import HTML
    except ImportError:
        HTML = None
    outputs = []
    for b in briefs:
        html_doc = render_one(b, score=b.get("score"))
        name = f"Brief {b['entreprise']} {date.today().isoformat()}"
        hp = os.path.join(out_dir, name + ".html")
        open(hp, "w", encoding="utf-8").write(html_doc)
        pp = None
        if HTML:
            pp = os.path.join(out_dir, name + ".pdf")
            HTML(string=html_doc).write_pdf(pp)
        outputs.append({"entreprise": b["entreprise"], "html": hp, "pdf": pp})
    print(json.dumps(outputs, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
