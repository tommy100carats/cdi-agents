#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generateur CV Tom Antonietti - gabarit deux colonnes (weasyprint)."""
import base64, os, sys, importlib.util
from weasyprint import HTML

NAVY = "#16243d"
GOLD = "#c6a24a"
GREY = "#6b7280"

CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ font-family: 'Liberation Sans', Arial, Helvetica, sans-serif; font-size: 7.9pt;
        color: #333; margin: 0; line-height: 1.32; }}
.header {{ background: {NAVY}; color: #fff; height: 32.4mm; padding: 0 8mm 0 6.7mm;
           display: flex; align-items: center; gap: 6.5mm; }}
.header img {{ width: 23.5mm; height: 23.5mm; object-fit: contain; flex: none; }}
.hname {{ font-size: 19pt; font-weight: bold; letter-spacing: .6pt; color: #fff; line-height: 1.05; }}
.htitle {{ color: {GOLD}; font-size: 8.6pt; font-weight: bold; margin-top: 1.6mm; }}
.hcontact {{ margin-top: 2.2mm; font-size: 7.3pt; color: #b1b9c4; }}
.hcontact span {{ color: #7d8798; margin: 0 1.8mm; }}
.body {{ position: relative; }}
.left {{ position: absolute; top: 5.5mm; left: 6.7mm; width: 60mm; }}
.right {{ margin: 5.5mm 6mm 6mm 73.6mm; padding-left: 5mm; border-left: .2mm solid #e2e2e2; }}
.left .sect {{ color: {GOLD}; font-size: 8pt; font-weight: bold; letter-spacing: 1.9pt;
               text-transform: uppercase; margin: 0 0 1.6mm 0; padding-bottom: 1mm;
               border-bottom: .3mm solid {GOLD}; }}
.right .sect {{ color: {NAVY}; font-size: 10.5pt; font-weight: bold; letter-spacing: 1.1pt;
                text-transform: uppercase; margin: 0 0 2mm 0; padding-bottom: 1.2mm;
                border-bottom: .25mm solid #b2b7bf; }}
.left .block {{ margin-bottom: 4.2mm; }}
.right .block {{ margin-bottom: 4.2mm; }}
ul {{ list-style: none; margin: 0; padding: 0; }}
li {{ position: relative; padding-left: 3mm; margin-bottom: 1.3mm; }}
li:before {{ content: '\\2022'; position: absolute; left: 0; top: -0.1mm; color: {GOLD};
             font-size: 8.5pt; line-height: 1.32; }}
.meta {{ color: #797979; }}
.profil {{ text-align: justify; }}
.xp {{ margin-bottom: 2.9mm; }}
.xp-head {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1.1mm; }}
.xp-post {{ color: {NAVY}; font-weight: bold; font-size: 8.5pt; }}
.xp-boite {{ color: {GOLD}; font-weight: bold; font-size: 8.5pt; }}
.xp-dates {{ color: #8a8a8a; font-size: 7.5pt; font-style: italic; white-space: nowrap; padding-left: 3mm; }}
.xp-activite {{ color: #797979; font-size: 7.4pt; font-style: italic; margin: -0.6mm 0 1mm 0; }}
.right li {{ text-align: justify; margin-bottom: 1.1mm; }}
b {{ color: #1c1c1c; font-weight: bold; }}
.right .xp b {{ color: #1c1c1c; }}
.left b {{ color: {NAVY}; }}
"""

def render(d, out_pdf):
    photo = ""
    if d.get("photo") and os.path.exists(d["photo"]):
        mime = "image/png" if d["photo"].lower().endswith(".png") else "image/jpeg"
        b64 = base64.b64encode(open(d["photo"], "rb").read()).decode()
        photo = f'<img src="data:{mime};base64,{b64}">'
    contacts = '<span>|</span>'.join(f" {c} " for c in d["contacts"])
    left = ""
    for titre, items in d["sidebar"]:
        lis = "".join(f"<li>{i}</li>" for i in items)
        left += f'<div class="block"><div class="sect">{titre}</div><ul>{lis}</ul></div>'
    def xp_html(x):
        lis = "".join(f"<li>{p}</li>" for p in x["puces"])
        return (f'<div class="xp"><div class="xp-head">'
                f'<div><span class="xp-post">{x["poste"]}</span> &mdash; '
                f'<span class="xp-boite">{x["boite"]}</span></div>'
                f'<div class="xp-dates">{x["dates"]}</div></div>'
                + (f'<div class="xp-activite">{x["activite"]}</div>' if x.get("activite") else '')
                + f'<ul>{lis}</ul></div>')
    t_profil = d.get("t_profil", "Profil"); t_xp = d.get("t_xp", "Expériences professionnelles"); t_asso = d.get("t_asso", "Projet associatif")
    bottom = ""
    if d.get("projets"):
        bottom = '<ul>' + "".join(f"<li>{p}</li>" for p in d["projets"]) + '</ul>'
    elif d.get("associatif"):
        bottom = xp_html(d["associatif"])
    right = (f'<div class="block"><div class="sect">{t_profil}</div><div class="profil">{d["profil"]}</div></div>'
             f'<div class="block"><div class="sect">{t_xp}</div>' + "".join(xp_html(x) for x in d["experiences"]) + '</div>'
             f'<div class="block"><div class="sect">{t_asso}</div>' + bottom + '</div>')
    doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
    <div class="header">{photo}<div><div class="hname">{d["nom"]}</div><div class="htitle">{d["titre"]}</div><div class="hcontact">{contacts}</div></div></div>
    <div class="body"><div class="left">{left}</div><div class="right">{right}</div></div></body></html>"""
    HTML(string=doc).write_pdf(out_pdf)
    print("->", out_pdf)

if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("cfg", sys.argv[1])
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    render(mod.DATA, mod.DATA.get("out", "CV.pdf"))
