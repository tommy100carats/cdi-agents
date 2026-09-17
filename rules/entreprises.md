# Registre des entreprises (bloc C de la grille, règle R11)

Hugo lit ce fichier pour le bloc C. Une ligne = un type prouvé, une source, une date. Une entreprise absente :
une recherche web unique (effectif, dernière levée, label), source citée dans le détail ; sinon C = 0 et
« entreprise à qualifier » dans le résumé du run. Noé liste chaque soir les entreprises à qualifier ; Tom valide,
la ligne s'ajoute par un commit. Jamais d'estimation : une ligne sans source n'existe pas.

Types et points : **scale-up financée** 4 · **grand groupe privé** 4 · **ETI en croissance** 3 · **ETI / PME
établie, organisme public ou parapublic, cabinet / ESN, filiale sans preuve** 2 · **petite structure identifiée** 1 ·
**non identifiable** 0.

## Prouvées (annonces du run du 07/09/2026, recherches web du 07/09/2026, mot de Tom)

| Entreprise | Type | C | Preuve | Source, date |
|---|---|---|---|---|
| Dust | scale-up financée | 4 | levée menée par Sequoia (2024) ; cible n°1 de Tom (« Dust c'est top ») | Tom, 07/09/2026 ; presse |
| Pennylane | scale-up financée | 4 | 1 200 salariés, 400 M€ levés dont Sequoia, Glassdoor 4,6 | annonce, 07/09/2026 |
| Alan | scale-up financée | 4 | 800+ salariés, 800 M€ d'ARR, 40 000 entreprises clientes | annonce, 07/09/2026 |
| Mistral AI | scale-up financée | 4 | IA-native, levées publiques récurrentes, licorne | annonce + presse, 07/09/2026 |
| Mirakl | scale-up financée | 4 | 750+ salariés, 9 bureaux, French Tech Next40 | annonce, 07/09/2026 |
| Sorare | scale-up financée | 4 | Series B 680 M$ (SoftBank, Accel), licorne | annonce, 07/09/2026 |
| ElevenLabs | scale-up financée | 4 | licorne IA, levées publiques 2024 et 2025 | presse, 07/09/2026 |
| Moments Lab (ex Newsbridge) | scale-up financée | 4 | Series A 7 M€ puis levée de 24 M$ ; série C annoncée (CFNEWS) | cfnews.net, gramond-avocats.com, 07/09/2026 |
| Veepee | grand groupe privé | 4 | 5 000 collaborateurs, 10 pays | annonce, 07/09/2026 |
| Cegid | grand groupe privé | 4 | leader européen des logiciels de gestion cloud, plusieurs milliers de salariés | site Cegid, 07/09/2026 |
| Thales | grand groupe privé | 4 | groupe coté, dizaines de milliers de salariés | connu, 07/09/2026 |
| Meilleurtaux | grand groupe privé | 4 | groupe, près de 300 agences, 650 recrutements annoncés pour 2025 | meilleurtaux.com (espace presse), 07/09/2026 |
| Nomadia | ETI en croissance | 3 | groupe adossé à Hg (investissement 2023), croissance par acquisitions | hgcapital.com, gpomag.fr, 07/09/2026 |
| ILLUIN Technology | ETI en croissance | 3 | Seven2 actionnaire majoritaire, 25 M€ investis (2024), Rueil-Malmaison | usine-digitale.fr, seven2.eu, 07/09/2026 |
| Bpifrance | organisme public ou parapublic | 2 | banque publique d'investissement | connu, 07/09/2026 |
| Caisse nationale de l'Assurance Maladie | organisme public | 2 | administration de la Sécurité sociale | connu, 07/09/2026 |
| NTT DATA | cabinet / ESN (client masqué, R6) | 2 | groupe mondial de services numériques, poste de consultant | annonce, 07/09/2026 |
| Esri France | filiale sans preuve d'effectif local | 2 | filiale française d'Esri (Meudon) | annuaire-entreprises.data.gouv.fr, 07/09/2026 |
| DFM | non identifiable | 0 | sigle sans site ni effectif lisible dans l'annonce | annonce, 07/09/2026 |
| Dataworks | non identifiable | 0 | aucune preuve lisible | annonce, 07/09/2026 |

## Grands groupes cotés (R19, 16/09/2026) : C = 4 et seuil go à 13

Groupes du CAC 40 et du SBF 120 dont le siège ou un grand site est à Paris ou à 30 minutes de la Mairie de Clichy,
et grandes entreprises cotées avec bureaux parisiens. Liste de départ, statut « coté » public et connu :
L'Oréal (Clichy), TotalEnergies (La Défense), Engie (La Défense), Saint-Gobain (La Défense), Capgemini, AXA,
BNP Paribas, Société Générale (La Défense), Crédit Agricole, LVMH, Kering, Hermès, Danone, Pernod Ricard, Orange,
Schneider Electric, Sanofi, Publicis, Bouygues, Vinci, Veolia, Thales, Safran, Airbus, Carrefour (Massy : hors
zone), Renault, Stellantis, Michelin, Legrand, Dassault Systèmes, Teleperformance, Edenred, Sodexo, Pluxee,
Accor, Bureau Veritas, Worldline, Ubisoft, Elis, SEB, BIC (Clichy), Imerys, Nexans, Rexel, Eiffage, Spie, Ipsos,
Sopra Steria, Atos, Amundi, Covivio, Klépierre. Cotées étrangères à Paris : Amazon, Google (Alphabet), Microsoft,
Meta, Apple, Salesforce, Oracle, SAP, IBM, Adobe, ServiceNow, Workday, Uber, Booking, Airbnb, Datadog, HubSpot,
NVIDIA, Accenture, Siemens Energy, Canonical (non cotée : à vérifier), Mirakl (non cotée : scale-up).
Ajouts du 17/09/2026 (runs de Léa) : RELX (LexisNexis), CANAL+ (groupe Vivendi puis Canal+ coté), Nestlé,
Roche, JCDecaux, VINCI (VINCI Energies, Cegelec). Hugo cite la source au premier usage.
Grands groupes non cotés à consulter au même titre (consigne de Tom, 17/09/2026 : « que les grands groupes ») :
Decathlon, Groupe Adeo (Leroy Merlin), Chanel, Lactalis, Auchan, Groupe Galeries Lafayette, Fnac Darty (cotée).
Accès connus au 17/09/2026 : L'Oréal et TotalEnergies (Avature, `careers.loreal.com/en_US/jobs/SearchJobs/<mot>`,
`jobs.totalenergies.com/fr_FR/careers/SearchJobs/<mot>`, filtrer le lieu sur la page de détail) ; Workday
(nvidia wd5, salesforce wd12, adobe wd5, thales wd3 Careers, pernodricard wd3, ag wd3 Airbus, accenture wd103,
michelinhr wd3, mastercard wd1, hp wd5, sanofi wd3, teleperformance wd1) ; Amazon (JSON). Bloqués pour le code
(403 ou rendu JavaScript) : Schneider Electric, BNP Paribas, Société Générale, Orange, Capgemini, Danone, Decathlon
(joinus.decathlon.fr) : passer par les alertes LinkedIn de Tom et par Indeed.
Hugo cite la source (bourse, site investisseurs) au premier usage et passe la ligne dans « Prouvées ».

## Présumées (sources ATS de `rules/sources.md`) : à confirmer au premier usage par une recherche web, source citée

Doctolib, Qonto, PhotoRoom, Notion, Ledger, Back Market, Ankorstore, Swan, Wellhub (Gympass), Algolia, TheFork,
Figma, Alma, Datadog, iBanFirst, Brevo, Malt, Pigment, 360Learning, Agicap, Contentsquare, Aircall, Swile : présumées
scale-up financée ou grand groupe privé (4). Joko, lemlist, Didomi, Doctrine : présumées ETI en croissance (3).
Une présomption ne donne pas les points : Hugo cite la source trouvée, puis la ligne passe dans « Prouvées ».
