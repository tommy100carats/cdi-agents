# Sources de sourcing — RevOps, Sales Ops, AI Ops (v3, 07/09/2026)

Ordre de fiabilité pour Léa : **(1) API d'ATS**, structurées, vérifiables par code ; **(2) alertes LinkedIn dans
Gmail**, à re-trouver ensuite sur une source vérifiable ; **(3) agrégateurs lisibles** ; **(4) boards
spécialisés** ; **(5) généralistes**. Pour chaque offre repérée sur une source non vérifiable (LinkedIn,
Welcome to the Jungle, Indeed), retrouver le lien direct avant toute suite.

## 1. API d'ATS (interroger directement, réponse JSON)

| ATS | URL | Slugs connus (à enrichir) |
|---|---|---|
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/<slug>` | dust, pennylane, alan, joko, photoroom, mistral.ai, doctolib, qonto, elevenlabs, notion, swile, payfit, spendesk, lemlist, pigment, fleet, jimmy, defacto |
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` | gympass (Wellhub), contentsquare, aircall, backmarket, ledger, deezer, mirakl, algolia, sorare, ankorstore, agicap, yousign, skello, partoo |
| Lever | `https://api.lever.co/v0/postings/<slug>?mode=json` | brevo, malt, didomi, pigment, veepee, 360learning, ornikar, lydia, october, shine, swan |
| Teamtailor | page carrière `<entreprise>.teamtailor.com/jobs` (HTML lisible) | kolecto, sunday, edflex, markentive |
| Welcome to the Jungle | non vérifiable par code (rendu JavaScript) | repérage seulement |
| Recruitee, Workable, SmartRecruiters, Taleez, WeRecruit | pages HTML lisibles | ouvrir la page directe |

Recherche à faire sur chaque board : `revenue operations`, `revops`, `sales operations`, `sales ops`,
`business operations`, `gtm operations`, `go-to-market`, `ai ops`, `ai operations`, `automation`,
`ai automation`, `ai enablement`, `ai adoption`, `ai transformation`, `no-code`, `workflow`, `enablement`,
`implementation manager`, `solutions consultant`.

## 2. LinkedIn, via les alertes Gmail

Requête Gmail : `from:jobalerts-noreply@linkedin.com OR from:jobs-listings@linkedin.com newer_than:3d`.
Lire `plaintextBody`, extraire titre / entreprise / lieu. Les liens `linkedin.com/comm/jobs/view/…` sont
authentifiés : jamais utilisés comme lien direct. Retrouver l'offre sur l'ATS ou le site carrière.

Alertes LinkedIn à maintenir côté Tom (une par intitulé, Paris + remote France) : Revenue Operations ·
RevOps Analyst · Sales Operations · Sales Ops Analyst · Business Operations · GTM Operations · AI Ops ·
AI Automation · Automation Specialist · AI Enablement · AI Adoption · Sales Enablement · Implementation Manager.

## 3. Agrégateurs lisibles et vérifiables (source de confirmation de secours)

- **Built In** (builtin.com) : titre, lieu, « Posted X days ago », télétravail et exigences en clair. C'est via
  Built In que l'offre Believe a été confirmée le 20/08/2026.
- **jobs.techstars.com** (rendu lisible).
- **Wellfound** (wellfound.com), **Y Combinator Work at a Startup** (workatastartup.com), **Otta**.
- **HelloWork**, **APEC** (apec.fr : les postes IA des ETI sortent là), **Cadremploi**, **Indeed** (via le
  connecteur Indeed quand il est disponible ; sinon repérage seulement).

## 4. Boards spécialisés

- **RevOps / Sales Ops** : RevOps Co-op job board, Pavilion, RevGenius Jobs, revopsroles.com, Modern Sales Pros,
  Bravado (bravado.co), RevPath / DealHub, albus (école RevOps, communauté française).
- **IA et startups** : ai-jobs.net, aijobs.net, Cord (cord.co), startup.jobs, France Digitale Job Board,
  Station F Jobs, EU-Startups Jobs, Sifted Jobs, Tech.eu Jobs, VivaTech Jobs, Welcome to the Jungle
  (repérage).
- **Cabinets et réseaux** : Elinoï, Ignition Program, Bureau des Talents, Mistertemp Cadres (repérage).

## 5. Entreprises cibles à surveiller nommément (pages carrière)

Fintech et SaaS français : Qonto, Pennylane, Alan, Dust, Doctolib, Swile, PayFit, Spendesk, Malt, Brevo,
Pigment, Mirakl, Contentsquare, Aircall, Ledger, Back Market, Deezer, Believe, Ornikar, Lydia, Sorare,
Ankorstore, Yousign, Agicap, Skello, Partoo, 360Learning, Lemlist, Sellsy, Axonaut, Kolecto, Edflex, Joko,
Photoroom, Mistral AI, ElevenLabs (Paris), Notion (Paris), Datadog (Paris), HubSpot (Paris), Salesforce (Paris,
postes non-Salesforce-admin), Adobe, Google (GTM), Microsoft (partner ops), SAP, Wavestone et cabinets IA (Sia,
Artefact, Onepoint) pour la famille 1.

## 6. Ce qui n'est pas une source

Un email personnel d'un recruteur sur contact@tomantonietti.com (hors périmètre de l'agent : signalé à Tom),
une annonce sans employeur identifiable (cabinet masqué : croiser avant, R6), un poste republié en boucle par
un agrégateur (clé métier identique : Doublon).
