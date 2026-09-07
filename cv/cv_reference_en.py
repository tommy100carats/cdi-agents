# -*- coding: utf-8 -*-
"""CV de référence, version anglaise (v3, 07/09/2026).

C'est le point de départ d'Inès : pour une annonce donnée, seuls le titre, l'accroche, l'ordre des
compétences et la hiérarchie des puces changent. Les faits et chiffres viennent de rules/profil.md.
Passe cv_check.py à 0 FAIL. À valider par Tom avant tout usage.
"""

DATA = {
    "out": "CV Tom Antonietti Reference EN.pdf",
    "nom": "TOM ANTONIETTI",
    "titre": "Revenue Operations · GTM workflows, automation &amp; AI agents",
    "contacts": ["tom.antonietti@gmail.com", "+33 6 31 77 91 06", "Paris · Driving licence",
                 "linkedin.com/in/tom-a-05431791", "github.com/tommy100carats"],
    "photo": "avatar.jpg",
    "t_profil": "Profile",
    "t_xp": "Professional experience",
    "t_asso": "Personal projects",
    "profil": (
        "A graduate of <b>emlyon business school</b> with seven years across sales and operations. "
        "My first reflex is to understand what can be improved: <b>observe the processes in place, talk "
        "to the teams, read the documentation</b>. Then simplify, tool up, automate. And measure, always, "
        "through the indicators and through what users say. I like solving problems and bringing a point "
        "of view to optimise what already exists, and those are the skills I want to put to work at "
        "<b>{{ENTREPRISE}}</b>. <b>Available immediately.</b>"
    ),
    "sidebar": [
        ("Education", [
            "<b>emlyon business school</b><br><span class='meta'>Master in Management (PGE) · 2016–2019</span>",
            "<b>INSEAD – CEDEP</b><br><span class='meta'>Live for Good programme · 2020–2021</span>",
            "<b>IAE Amiens</b><br><span class='meta'>M1 Management &amp; Entrepreneurship · 2013–2016</span>",
            "<b>IUT Amiens</b><br><span class='meta'>Two-year degree, Sales &amp; Marketing · 2011–2013</span>",
        ]),
        ("Core skills", [
            "<b>GTM workflow ownership</b>: routing, hand-offs, renewals",
            "<b>CRM administration</b>: pipeline, stages, data hygiene",
            "<b>Workflow automation</b>: triggers, error handling",
            "<b>AI agents</b>: tool calling, guardrails, human gates",
            "<b>Reporting &amp; KPIs</b>: dashboards, gap analysis, action plans",
            "<b>Business partnering</b>: influence without authority",
            "<b>Project ownership</b>: scoping, sequencing, shipping",
        ]),
        ("Tools", [
            "Automation: <b>n8n</b>, <b>Make</b>, <b>Zapier</b>, <b>Airtable</b>, <b>Process Street</b>",
            "Integrations: webhooks and APIs, no-code",
            "AI: <b>Claude</b>, <b>Dust</b>, <b>ChatGPT</b>, LLM APIs",
            "CRM: <b>Digiforma</b>, <b>BoondManager</b>, HubSpot (certified), Salesforce (basics)",
            "Data / BI: <b>Power BI</b>, advanced <b>Excel</b>, <b>SAP</b>, Postgres (Supabase)",
            "Process: <b>Notion</b> (API)",
        ]),
        ("Languages", [
            "<b>French</b>: native",
            "<b>English</b>: fluent (910 TOEIC)",
            "<b>Spanish</b>: intermediate",
        ]),
        ("Certifications", [
            "<b>HubSpot</b>: Revenue Operations &amp; Reporting",
            "<b>HubSpot</b>: Sales Management &amp; Sales Hub",
            "<b>Kaggle</b>: Advanced SQL &amp; Intro to SQL",
        ]),
        ("Interests", [
            "Tennis (ranked 15/4), basketball, football",
            "Yoga, meditation, chess",
        ]),
    ],
    "experiences": [
        {
            "poste": "Head of Operations, Sales &amp; AI",
            "boite": "CITYZ'Formation",
            "dates": "Oct. 2023 – May 2026",
            "activite": "EdTech start-up: apprenticeship centre and corporate training, built from launch",
            "puces": [
                "<b>Owned the workflow end to end</b>: designed the sales cycle, then everything that happens "
                "once a deal is signed, written down as <b>23 documented steps</b> (onboarding, contracting, "
                "e-signature, filing with the third-party funder and handling its rejections, mandatory "
                "regulatory documents, branches for missing paperwork and terminations). <b>Run on 143 "
                "files</b>: from 2 hours to 30 minutes per file, far fewer errors, an identical audit trail every time.",
                "<b>Removed operational friction</b>: configured and rolled out the CRM end to end (pipeline, "
                "stages, invoicing, reporting), then replaced manual steps with automated workflows on Process "
                "Street and n8n (follow-ups, triggers, scoring, webhooks and APIs to the CRM, error handling).",
                "<b>Reporting leadership could trust</b>: defined and tracked the KPI set (conversion, cycle "
                "length, file volume, productivity), gap analysis and action plans with management. Responsible "
                "for the centre's revenue: <b>€3M</b> since launch.",
                "<b>Business partner without authority</b>: coordinated <b>5 people</b> in admin, academic and "
                "legal, none of whom reported to me.",
                "<b>Retention and expansion</b>: <b>20 corporate accounts</b>; <b>40 % expanded</b> onto a "
                "second offer and <b>25 % renewed</b>, up to <b>8 people trained in one year</b> at a single account.",
            ],
        },
        {
            "poste": "Business Engineer",
            "boite": "5 Degrés",
            "dates": "Oct. 2022 – Oct. 2023",
            "activite": "IT services firm: consulting, delivery and consultant placement with large accounts",
            "puces": [
                "<b>€360K revenue generated, 120 % of target</b>, an average of <b>€180K per account opened</b> "
                "on a long B2B cycle with technical buyers, including <b>SNCF Connect &amp; Tech</b>.",
                "<b>Pipeline and data ownership</b> on the CRM: accounts, deals, staffing, invoicing, forecast "
                "reliability and data hygiene.",
            ],
        },
        {
            "poste": "Founder &amp; Consultant",
            "boite": "Freelance · SMEs",
            "dates": "May 2021 – Sept. 2022",
            "activite": "Own consulting practice: commercial and operational structuring for small businesses",
            "puces": [
                "<b>Built my own client practice</b>: found the clients, priced the work and carried the risk. "
                "Diagnosed how each business actually ran, then rebuilt its funnel and its operating routines. "
                "Les Ruchers du Valois: <b>€350K revenue</b> (2021). Savane &amp; Mousson: <b>+15 % average basket</b>.",
            ],
        },
        {
            "poste": "Junior Key Account Manager",
            "boite": "DIM (HanesBrands group)",
            "dates": "2019 – 2021",
            "activite": "Lingerie and hosiery: market-leading brand in French mass retail, HanesBrands group",
            "puces": [
                "<b>Data &amp; reporting</b>: owned reporting on <b>€20M revenue</b> (<b>Carrefour</b>, <b>Cora</b>) "
                "in Power BI and SAP; sell-out data, forecasting, promo tracking; <b>200+ SKUs</b> analysed.",
            ],
        },
    ],
    "projets": [
        "<b>AI agents for my own job search</b> (2026): a chain of seven agents (sourcing, scoring, company brief, "
        "CRM, control, CV) on Claude, Notion and Dust. The work is in the design: prompts, <b>tool calling</b>, "
        "connectors (Notion, Gmail), JSON schemas and <b>guardrails</b>, with human validation before any "
        "irreversible action. Deterministic checks in code; no production code written by me. Published on GitHub.",
        "<b>Mentalizi</b>: mobile app giving athletes personalised mental preparation through AI, built no-code "
        "(Replit) on a Postgres backend (Supabase).",
    ],
}
