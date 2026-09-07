# -*- coding: utf-8 -*-
"""CV de référence, version française (v3, 07/09/2026). Mêmes faits que la version anglaise.
Passe cv_check.py à 0 FAIL une fois {{ENTREPRISE}} remplacé. À valider par Tom avant tout usage."""

DATA = {
    "out": "CV Tom Antonietti Reference FR.pdf",
    "nom": "TOM ANTONIETTI",
    "titre": "Revenue Operations · workflows GTM, automatisation &amp; agents IA",
    "contacts": ["tom.antonietti@gmail.com", "06 31 77 91 06", "Paris · Permis B",
                 "linkedin.com/in/tom-a-05431791", "github.com/tommy100carats"],
    "photo": "avatar.jpg",
    "t_profil": "Profil",
    "t_xp": "Expériences professionnelles",
    "t_asso": "Projets personnels",
    "profil": (
        "Diplômé d'<b>emlyon business school</b>, sept ans entre la vente et les opérations. Mon premier "
        "réflexe, c'est de comprendre ce qu'on peut améliorer : <b>observer les process en place, échanger avec "
        "les équipes, lire la documentation</b>. Viennent ensuite la simplification, l'outillage et "
        "l'automatisation. Et la mesure, toujours, par les indicateurs et par les retours des utilisateurs. "
        "J'aime résoudre des problèmes et apporter ma vision pour optimiser ce qui existe déjà : c'est ce que je "
        "veux mettre au service de <b>{{ENTREPRISE}}</b>. <b>Disponible immédiatement.</b>"
    ),
    "sidebar": [
        ("Formation", [
            "<b>emlyon business school</b><br><span class='meta'>Programme Grande École · 2016–2019</span>",
            "<b>INSEAD – CEDEP</b><br><span class='meta'>Programme Live for Good · 2020–2021</span>",
            "<b>IAE Amiens</b><br><span class='meta'>M1 Management &amp; Entrepreneuriat · 2013–2016</span>",
            "<b>IUT Amiens</b><br><span class='meta'>DUT Techniques de Commercialisation · 2011–2013</span>",
        ]),
        ("Compétences clés", [
            "<b>Pilotage des workflows GTM</b> : routage, passages de relais, renouvellements",
            "<b>Administration CRM</b> : pipeline, étapes, qualité des données",
            "<b>Automatisation</b> : déclencheurs, gestion d'erreurs",
            "<b>Agents IA</b> : tool calling, garde-fous, validation humaine",
            "<b>Reporting &amp; KPI</b> : tableaux de bord, analyse d'écarts, plans d'action",
            "<b>Business partnering</b> : influence sans lien hiérarchique",
            "<b>Conduite de projet</b> : cadrage, séquencement, livraison",
        ]),
        ("Outils", [
            "Automatisation : <b>n8n</b>, <b>Make</b>, <b>Zapier</b>, <b>Airtable</b>, <b>Process Street</b>",
            "Intégrations : webhooks et API, no-code",
            "IA : <b>Claude</b>, <b>Dust</b>, <b>ChatGPT</b>, API de LLM",
            "CRM : <b>Digiforma</b>, <b>BoondManager</b>, HubSpot (certifié), Salesforce (notions)",
            "Data / BI : <b>Power BI</b>, <b>Excel</b> avancé, <b>SAP</b>, Postgres (Supabase)",
            "Process : <b>Notion</b> (API)",
        ]),
        ("Langues", [
            "<b>Français</b> : natif",
            "<b>Anglais</b> : courant (910 TOEIC)",
            "<b>Espagnol</b> : intermédiaire",
        ]),
        ("Certifications", [
            "<b>HubSpot</b> : Revenue Operations &amp; Reporting",
            "<b>HubSpot</b> : Sales Management &amp; Sales Hub",
            "<b>Kaggle</b> : Advanced SQL &amp; Intro to SQL",
        ]),
        ("Centres d'intérêt", [
            "Tennis (classé 15/4), basket, football",
            "Yoga, méditation, échecs",
        ]),
    ],
    "experiences": [
        {
            "poste": "Responsable des Opérations, Sales &amp; IA",
            "boite": "CITYZ'Formation",
            "dates": "Oct. 2023 – Mai 2026",
            "activite": "Start-up EdTech : CFA et formation continue, construite depuis le lancement",
            "puces": [
                "<b>Pilotage du workflow de bout en bout</b> : conception du cycle de vente, puis de tout ce qui "
                "suit la signature, écrit en <b>23 étapes documentées</b> (onboarding, contractualisation, "
                "signature électronique, dépôt auprès du tiers financeur et traitement de ses rejets, pièces "
                "réglementaires, branches pour pièces manquantes et ruptures). <b>Exécuté sur 143 dossiers</b> : "
                "de 2 heures à 30 minutes par dossier, forte réduction des erreurs, même dossier de preuves à chaque fois.",
                "<b>Suppression des frictions opérationnelles</b> : CRM configuré et déployé de bout en bout "
                "(pipeline, étapes, facturation, reporting), puis remplacement des étapes manuelles par des workflows "
                "Process Street et n8n (relances, déclencheurs, scoring, webhooks et API vers le CRM, gestion d'erreurs).",
                "<b>Un reporting fiable pour la direction</b> : définition et suivi des KPI (conversion, durée de cycle, "
                "volume de dossiers, productivité), analyses d'écarts et plans d'action. Responsable du chiffre "
                "d'affaires du centre : <b>3 M€</b> depuis le lancement.",
                "<b>Business partner sans lien hiérarchique</b> : coordination de <b>5 personnes</b> (administratif, "
                "pédagogie, juridique).",
                "<b>Fidélisation et développement</b> : <b>20 comptes entreprises</b> ; <b>40 %</b> convertis sur une "
                "offre additionnelle et <b>25 %</b> reconduits, jusqu'à <b>8 salariés formés en un an</b> sur un compte.",
            ],
        },
        {
            "poste": "Ingénieur d'affaires",
            "boite": "5 Degrés",
            "dates": "Oct. 2022 – Oct. 2023",
            "activite": "ESN : conseil, delivery et placement de consultants auprès de grands comptes",
            "puces": [
                "<b>360 k€ de chiffre d'affaires, 120 % des objectifs</b>, <b>180 k€ par compte ouvert</b> sur un cycle "
                "B2B long avec des acheteurs techniques, dont <b>SNCF Connect &amp; Tech</b>.",
                "<b>Pipeline et données</b> sur le CRM : comptes, affaires, staffing, facturation, fiabilité du "
                "forecast et qualité des données.",
            ],
        },
        {
            "poste": "Consultant &amp; Formateur indépendant",
            "boite": "PME",
            "dates": "Mai 2021 – Sept. 2022",
            "activite": "Pratique montée en propre : structuration commerciale et opérationnelle de petites entreprises",
            "puces": [
                "<b>Clientèle constituée seul</b>, prix fixés, risque porté. Diagnostic du fonctionnement réel de chaque "
                "entreprise, puis reconstruction de son funnel et de ses routines. Les Ruchers du Valois : "
                "<b>350 k€ de CA</b> (2021). Savane &amp; Mousson : <b>+15 % de panier moyen</b>.",
            ],
        },
        {
            "poste": "Key Account Manager Junior",
            "boite": "DIM (groupe HanesBrands)",
            "dates": "2019 – 2021",
            "activite": "Lingerie et collants : marque leader de la grande distribution française",
            "puces": [
                "<b>Data &amp; reporting</b> : reporting sur <b>20 M€ de CA</b> (<b>Carrefour</b>, <b>Cora</b>) sous "
                "Power BI et SAP ; sell-out, prévisions, suivi promotionnel ; <b>200+ SKU</b> analysés.",
            ],
        },
    ],
    "projets": [
        "<b>Agents IA pour ma propre recherche d'emploi</b> (2026) : une chaîne de sept agents (sourcing, notation, "
        "brief entreprise, CRM, contrôle, CV) sur Claude, Notion et Dust. Le travail est dans la conception : prompts, "
        "<b>tool calling</b>, connecteurs (Notion, Gmail), schémas JSON et <b>garde-fous</b>, avec validation humaine "
        "avant toute action irréversible. Contrôles déterministes en code ; aucun code de production écrit par moi. "
        "Publié sur GitHub.",
        "<b>Mentalizi</b> : application mobile de préparation mentale pour sportifs, personnalisée par l'IA, construite "
        "en no-code (Replit) sur un backend Postgres (Supabase).",
    ],
}
