# Sources de sourcing, Sales Ops, AI Ops, RevOps junior (v4, 16/09/2026)

Ordre de fiabilité pour Léa : **(1) API d'ATS**, structurées, vérifiables par code ; **(2) alertes LinkedIn dans
Gmail** ; **(3) agrégateurs lisibles** ; **(4) boards spécialisés** ; **(5) généralistes**. Pour une offre repérée
sur une source que le code ne sait pas lire (LinkedIn, Welcome to the Jungle, Indeed), chercher d'abord le lien
ATS ou site carrière ; sinon garder ce lien tel quel : il est acceptable, l'offre passe avec « Actif vérifié :
Non vérifiable » et un texte partiel signalé. Non vérifiable n'est jamais un motif d'écart.

## 1. API d'ATS (interroger directement, réponse JSON)

| ATS | URL | Slugs connus (à enrichir) |
|---|---|---|
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/<slug>` | vérifiés le 07/09 : dust, pennylane, alan, joko, photoroom, mistral.ai, doctolib, qonto, elevenlabs, notion, lemlist, illuin, ledger, backmarket, sorare, ankorstore, swan (en 404 : swile, payfit, pigment, fleet, jimmy, defacto, spendesk vide) |
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` (ou `boards-api.eu.greenhouse.io`) | vérifiés le 07/09 : gympass (Wellhub), mirakl, algolia, thefork, figma, alma31 (Alma, EU), datadog, ibanfirst (en 404 : contentsquare, aircall, backmarket, ledger, deezer, sorare, ankorstore, agicap, yousign, skello, partoo) |
| Lever | `https://api.lever.co/v0/postings/<slug>?mode=json` | vérifiés le 07/09 : brevo, malt, didomi, pigment, veepee, 360learning, qonto, agicap, contentsquare, aircall, swile, doctrine (en 404 : ornikar, lydia, october, shine, swan) |
| Teamtailor | page carrière `<entreprise>.teamtailor.com/jobs` (HTML lisible) | kolecto, sunday, edflex, markentive |
| Welcome to the Jungle | non vérifiable par code (rendu JavaScript) | repérage seulement |
| Recruitee, Workable, SmartRecruiters, Taleez, WeRecruit | pages HTML lisibles | ouvrir la page directe |

Recherche à faire sur chaque board : `revenue operations`, `revops`, `sales operations`, `sales ops`,
`business operations`, `gtm operations`, `ai ops`, `ai operations`, `automation`, `ai automation`,
`ai adoption`, `no-code`, `workflow`, `operations analyst`, `operations specialist`, `operations associate`,
`sales analyst`, `revenue analyst`, `commercial operations`, `junior`, `chargé(e) d'opérations commerciales`,
`analyste performance commerciale`, `sales excellence`, `sales effectiveness`.

## 2. LinkedIn, via les alertes Gmail

Requête Gmail : `from:jobalerts-noreply@linkedin.com OR from:jobs-listings@linkedin.com newer_than:3d`.
Lire `plaintextBody`, extraire titre / entreprise / lieu. Les liens `linkedin.com/comm/jobs/view/…` sont
acceptés comme lien direct (le code ne peut pas les lire : pas de scraping LinkedIn). Chercher d'abord l'offre
sur l'ATS ou le site carrière pour le texte intégral ; à défaut, garder le lien LinkedIn et le texte de l'alerte.

Alertes LinkedIn à maintenir côté Tom (une par intitulé, Paris + remote France, filtre « Premier emploi,
Confirmé » et non « Directeur ») : Sales Operations Analyst · Sales Operations Specialist · Business Operations
Analyst · Revenue Operations Analyst · RevOps junior · AI Ops · AI Automation · Automation Specialist ·
Chargé d'opérations commerciales · Analyste performance commerciale.

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

## 5 bis. Grands groupes cotés (priorité depuis le 16/09/2026, R19 ; tous à chaque run, R25)

Léa consulte **tous** les groupes de la liste à chaque run de production (budget 30 min pour cette étape ; si le
budget est dépassé, elle reprend au prochain run là où elle s'est arrêtée et le note dans Contrôles).

Pages carrière des groupes de `rules/entreprises.md` (section « Grands groupes cotés »), recherche « sales
operations », « sales ops », « business operations », « revenue operations », « analyste commercial »,
« performance commerciale », « sales excellence », « ai ops », « automatisation ». ATS fréquents : Workday
(`<groupe>.wd3.myworkdayjobs.com`, pages lisibles), SuccessFactors, Taleo, Eightfold. Amazon :
`https://www.amazon.jobs/en/search.json?base_query=<requête>&loc_query=Paris` (JSON lisible). Google :
`careers.google.com` (recherche Paris). Microsoft : `jobs.careers.microsoft.com` (Paris). Toujours vérifier le lieu
(R21) et la séniorité (R17) : les grands groupes publient beaucoup d'intitulés « Senior » hors cible.

Accès vérifiés le 17/09/2026 (recherche POST Workday `https://<tenant>.<wdN>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/jobs`,
corps `{"searchText": "...", "limit": 20, "offset": 0, "appliedFacets": {}}`) : nvidia wd5, salesforce wd12,
adobe wd5 (external_experienced), thales wd3 (Careers), pernodricard wd3 (pernod-ricard), ag wd3 (Airbus),
accenture wd103, michelinhr wd3, mastercard wd1, hp wd5, sanofi wd3 (SanofiCareers), teleperformance wd1.
Tenant existant, nom de site à trouver sur la page carrière (réponse 422) : schneiderelectric wd3, danone wd3,
engie wd3. Capgemini : JSON `https://www.capgemini.com/wp-json/macs/v1/jobs?country_code=fr-fr&search=<mot>&size=50`.
L'Oréal et TotalEnergies : Avature (voir rules/entreprises.md). BNP Paribas, Société Générale, Orange, Decathlon :
pas d'accès par le code, passer par Indeed et les alertes LinkedIn. Un accès trouvé en cours de run se note dans
Contrôles pour être ajouté ici.

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
