# Critères de recherche et grille de notation — v3 (07/09/2026)

Source de vérité unique pour Léa (sourcing) et Hugo (notation). Modifier ici, jamais dans un prompt.
Toute correction de Tom devient une règle numérotée en fin de document (registre), datée, jamais rediscutée.

## 1. Périmètre (appliqué par Léa, avant toute note)

- **CDI uniquement.** Un CDD, une mission, une franchise, un stage : ligne Inbox « Écartée », raison écrite.
- **Géographie** : Paris et très proche banlieue pour les postes sur site ou hybrides ; full remote accepté,
  y compris depuis un autre pays (Europe, EMEA, worldwide). Écarter d'office : Montigny-le-Bretonneux (78),
  l'Essonne (91), tout trajet quotidien déraisonnable depuis Paris.
- **Familles, par ordre de priorité** : (1) AI Ops / automatisation IA côté business, sans exigence de
  développement logiciel ; (2) Revenue Operations ; (3) Sales Ops, Business Ops ; (4) Enablement, commercial
  inbound ; (5) autres postes projet ou produit hors tech quand le secteur parle au parcours (formation,
  éducation, sport). Également acceptés : Sales Enablement, PMO, Account Manager, Customer Success, Team Lead
  SDR si le coaching est réel.
- **Séniorité (règle R8)** : cible = postes demandant **moins de 3 ans en opérations** (« coeur »).
  **3 à 5 ans passent aussi, au cas où** (« stretch », signalé, jamais pénalisé). Plus de 5 ans : « hors »,
  écartée avec raison. Aucune durée écrite : « inconnu », retenue et signalée. Le calcul est fait par
  `pipeline/seniority.py`, pas par le modèle.
- **Exclusions fermes** (Écartée, jamais notée) : quotidien fait de prospection outbound à froid ; code de
  production, pipelines de données, profil Data Scientist / ML Engineer / Software Engineer, diplôme
  d'ingénieur exigé, LangChain, LangGraph, CI-CD, AWS. Tom ne code pas, par choix.
- **Vérification d'activité** : une offre n'est présentée comme active que si `pipeline/link_check.py` l'a
  confirmée (API ATS ou page lisible). LinkedIn et Welcome to the Jungle ne se vérifient pas : chercher le lien
  direct (ATS, site carrière, Built In) ; sinon « Non vérifiable », étape « En veille ».

## 2. Profil réel de Tom (ne jamais gonfler, ne jamais retirer)

Voir `rules/profil.md` pour les faits et chiffres. Pour la notation, retenir :
- Expérience commerciale et opérationnelle ~7 ans, dont **2 ans 8 mois en opérations** (CITYZ'Formation,
  oct. 2023 → mai 2026) : responsable commercial, opérations et IA, process en 23 étapes sur 143 dossiers,
  CRM déployé de bout en bout (Digiforma), reporting KPI, coordination de 5 personnes sans lien hiérarchique.
- Outils en pratique professionnelle : Digiforma, BoondManager, Power BI, Excel avancé, SAP, Process Street,
  n8n, Make, Zapier, Airtable, Notion (API), Zoho Campaigns, Meta Ads.
- **HubSpot : certifié (4 certifications), jamais en production. Salesforce : notions, jamais en production.**
  Une certification sans pratique professionnelle est toujours « partiel », jamais « couvert ».
- **SQL** : certifié Kaggle, base Postgres (Supabase) en production sur Mentalizi, requêtes générées par l'IA puis
  relues. Jamais « SQL avancé ».
- **Agents IA et automatisation en opérations** : système personnel réel (Claude + Notion, puis Dust), documenté.
- **« Avoir architecté un CRM »** : le critère porte sur l'acte, pas la marque. Un CRM déployé de bout en bout sur
  un autre outil compte comme couvert, marque signalée en réserve.
- Formation d'adultes et conduite du changement : réelles (formateur, référent IA).
- Anglais courant (910 TOEIC). Aucune expérience de comité de direction en anglais dans un grand groupe matriciel.

## 3. Grille de notation v3, sur 20, additive, sans malus (règle R7)

**Aucun malus.** Une exigence absente vaut 0 dans la couverture et c'est tout. Les exclusions fermes sont
traitées en sourcing, avant la note. Une donnée introuvable (effectif, salaire, avis) laisse le point à 0 et
le champ vide ; on n'estime jamais.

| Bloc | Points | Comment |
|---|---|---|
| **A. Couverture des exigences écrites** | /10 | Chaque exigence de l'annonce : couvert 1, partiel 0,5, absent 0. Total ramené sur 10. Quand l'annonce publie ses indicateurs de succès, ce sont eux la liste, pas les compétences. |
| **B. Conditions** | /3 | +1 CDI et lieu compatibles (Paris, proche banlieue, remote) · +1 télétravail hybride ou remote, ou Paris intra-muros · +1 salaire affiché ≥ 50 k€, ou non affiché mais fourchette de marché plausible. |
| **C. Entreprise** | /4 | +1 grand groupe, ETI ou effectif ≥ 500 · +1 entreprise ambitieuse : levée de fonds < 18 mois, croissance forte, IA-native, scale-up financée · +1 réputation employeur (Glassdoor ≥ 4 ou label reconnu) · +1 écosystème qui parle au parcours (SaaS B2B, fintech, edtech / formation, comptable / TPE-PME, retail). |
| **D. Différenciateurs demandés** | /3 | +1 chacun, seulement si l'annonce le demande explicitement ET que Tom l'a : agents IA / automatisation en opérations · formation ou enablement d'adultes · outil nommé que Tom pratique (n8n, Make, Zapier, HubSpot, Dust, Notion, Airtable, Process Street). |

**Note = A + B + C + D**, entière, plafonnée à 20. En cas d'hésitation entre deux notes, prendre la basse et
l'écrire dans le détail.

**Bande séniorité** : affichée dans le détail (coeur / stretch / inconnu), sans effet sur la note (R8).

## 4. Seuils et effets

| Note | Verdict | Effet dans la chaîne |
|---|---|---|
| 15 à 20 | go_prioritaire | Camille rédige le brief, Scribe crée la fiche CRM « À contacter », priorité Haute (famille 1) ou Moyenne |
| 12 à 14 | veille | Reste dans Inbox « En veille » ; visible dans le pipeline du mardi et du vendredi ; pas de brief |
| 0 à 11 | no_go | Inbox « Écartée », raison écrite ; rien ne va au CRM |
| — | dossier_ouvert | Un dossier est déjà ouvert chez cette entreprise : verdict rendu, note calculée, mais Scribe ne crée rien et écrit l'avertissement |

Un doute exprimé par Hugo (annonce incomplète, deux notes possibles) fait descendre au seuil inférieur et
s'écrit dans le détail.

## 5. Sortie attendue de Hugo (validée par `schemas/verdict.json`)

Verdict en une phrase ; tableau de couverture (exigence | preuve | couvert / partiel / absent | centrale) ;
liste des exigences sans preuve, sans adoucir ; les quatre sous-scores ; la note ; dans un bloc séparé et
annoncé comme tel, les déductions sur l'entreprise ou le poste ; la liste des règles du registre appliquées.
Ne jamais rédiger de CV ni de lettre.

## 6. Registre des corrections (numéroté, daté, jamais rediscuté)

- **R1 (14/08/2026)** : une expérience d'agents IA exigée n'est plus un motif de plafond ni de rejet.
- **R2 (30/08/2026)** : privilégier les niveaux Analyst, Associate, Specialist, Coordinator, Junior,
  « Chargé(e) de » ; Manager si 3 à 6 ans demandés ; Manager en cabinet exigeant 6 ans et plus de conseil,
  dé-priorisé.
- **R3 (01/09/2026)** : un vide n'est pas un zéro. Une donnée manquante ne pénalise pas, elle se laisse vide.
- **R4 (01/09/2026)** : jamais de double comptage entre couverture et autre chose. (La règle de plafond à 12
  qui existait alors est **abrogée par R7**.)
- **R5 (02/09/2026)** : toute exigence de langage ou de framework de code est une exigence absente dans la
  couverture ; si elle est centrale au poste, c'est une exclusion ferme traitée en sourcing.
- **R6 (02/09/2026)** : un cabinet masque le nom du client ; croiser lieu, rattachement, stack et fourchette
  avant de conclure qu'une offre est neuve (vérification par clé métier + dossier ouvert).
- **R7 (07/09/2026)** : **pas de malus.** La grille est purement additive. Les signaux négatifs (Salesforce
  hands-on exigé, SQL quotidien avec dbt, management lourd, > 30 % de déplacements) pèsent uniquement par
  les points de couverture qu'ils font perdre.
- **R8 (07/09/2026)** : **séniorité** : coeur ≤ 3 ans en opérations ; 3 à 5 ans acceptés « au cas où » sans
  pénalité ; > 5 ans écartés au sourcing ; inconnu accepté et signalé.
- **R9 (07/09/2026)** : **bonus entreprise explicites** : grand groupe (+1) et entreprise ambitieuse (+1) sont
  des points de la grille, pas des impressions ; ils exigent une preuve (effectif public, levée datée, actualité).

*Les règles suivantes seront extraites des 20 offres de calibration (voir `docs/calibration.md`).*
