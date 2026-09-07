# Critères de recherche et grille de notation, v3.1 (calibrée le 07/09/2026)

Source de vérité unique pour Léa (sourcing) et Hugo (notation). Modifier ici, jamais dans un prompt.
Toute correction de Tom devient une règle numérotée en fin de document (registre), datée, jamais rediscutée.

## 1. Périmètre (appliqué par Léa, avant toute note)

- **CDI uniquement.** Un CDD, une mission, une franchise, un stage : ligne Inbox « Écartée », raison écrite.
- **Géographie** : Paris et très proche banlieue pour les postes sur site ou hybrides ; full remote accepté,
  y compris depuis un autre pays (Europe, EMEA, worldwide). Écarter d'office : Montigny-le-Bretonneux (78),
  l'Essonne (91), tout trajet quotidien déraisonnable depuis Paris.
- **Périmètre (précisé par Tom le 07/09/2026)** : tout ce qui touche aux opérations, de 0 à 5 ans d'expérience
  demandés. **Familles, par ordre de priorité** : (1) AI Ops / automatisation IA côté business, sans exigence de
  développement logiciel ; (2) Revenue Operations ; (3) Sales Ops, Business Ops ; (4) **Customer Success Manager**
  (CSM, account management) ; (5) Enablement, commercial inbound ; (6) autres postes projet ou produit hors tech
  quand le secteur parle au parcours (formation, éducation, sport). Également acceptés : Sales Enablement, PMO,
  Team Lead SDR si le coaching est réel.
- **Séniorité (règle R8, précisée le 07/09)** : cible = postes demandant **de 0 à 5 ans d'expérience**. Deux
  bandes retenues, sans effet sur la note : « coeur » (≤ 3 ans) et « stretch » (3 à 5 ans, signalé). Plus de
  5 ans : « hors », écartée avec raison. Aucune durée écrite : « inconnu », retenue et signalée. Le calcul est
  fait par `pipeline/seniority.py` (années écrites d'abord, puis mot de niveau dans le titre), pas par le modèle.
- **Exclusions fermes** (Écartée, jamais notée) : quotidien fait de prospection outbound à froid ; code de
  production, pipelines de données, profil Data Scientist / ML Engineer / Software Engineer, diplôme
  d'ingénieur exigé, LangChain, LangGraph, CI-CD, AWS. Tom ne code pas, par choix. Les deux premières exclusions
  lisibles (diplôme d'ingénieur ou d'informatique exigé sans alternative commerce, code au coeur du poste) sont
  détectées par `python3 -m pipeline.cli exclusions annonce.txt`, phrase citée (R16).
- **Vérification d'activité** : une offre n'est présentée comme active que si `pipeline/link_check.py` l'a
  confirmée (API ATS ou page lisible). LinkedIn et Welcome to the Jungle ne se vérifient pas par le code : chercher le
  lien ATS ou site carrière ; sinon « Non vérifiable », et l'offre passe quand même (notation, brief, CRM), jamais
  présentée comme active.

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

## 3. Grille de notation v3.1, sur 20, additive, sans malus (règle R7)

**Aucun malus.** Une exigence absente vaut 0 dans la couverture et c'est tout. Les exclusions fermes sont
traitées en sourcing, avant la note. On n'estime jamais : un salaire absent ne coûte rien (R12), une entreprise
absente du registre se cherche une fois sur le web, source citée, sinon C vaut 0 et l'entreprise est à qualifier (R11).

| Bloc | Points | Comment |
|---|---|---|
| **A. Couverture des exigences écrites** | /10 | Chaque exigence de l'annonce : couvert 1, partiel 0,5, absent 0. Total ramené sur 10. Quand l'annonce publie ses indicateurs de succès, ce sont eux la liste, pas les compétences. |
| **B. Conditions** | /3 | +1 CDI · +1 lieu compatible (Paris, proche banlieue accessible, ou remote) · +1 salaire : point acquis sauf si un salaire affiché est inférieur à 50 k€ (on n'estime jamais). Le télétravail est affiché dans le détail, sans effet sur la note (R12). |
| **C. Entreprise** | /4 | **Le type d'entreprise fait la note (R11)**, prouvé par `rules/entreprises.md` ou par l'annonce : **4** scale-up financée (levée VC publique datée, Next40 / FT120, licorne) ou grand groupe privé (≥ 1 000 salariés, coté, groupe international) · **3** ETI en croissance (250 à 999 salariés, adossement ou croissance documentés) · **2** ETI ou PME établie, organisme public ou parapublic, cabinet / ESN (client masqué, R6), filiale française sans preuve d'effectif local · **1** petite structure identifiée (< 100 salariés) sans levée · **0** entreprise non identifiable. |
| **D. Différenciateurs demandés** | /3 | +1 chacun, seulement si l'annonce le demande explicitement ET que Tom l'a : agents IA / automatisation en opérations · formation ou enablement d'adultes · outil nommé que Tom pratique (n8n, Make, Zapier, HubSpot, Dust, Notion, Airtable, Process Street). |

**Note = A + B + C + D**, entière (arrondi vers le bas), plafonnée à 20. En cas d'hésitation entre deux notes,
prendre la basse et l'écrire dans le détail. **Texte partiel** : A plafonné à 6/10, B et C sur les faits publics (R15).

**Bande séniorité** : affichée dans le détail (coeur / stretch / inconnu), sans effet sur la note (R8).

## 4. Seuils et effets

| Note | Verdict | Effet dans la chaîne |
|---|---|---|
| 15 à 20 | go_prioritaire | Camille rédige le brief, Scribe crée la fiche CRM « À contacter », priorité Haute (famille 1) ou Moyenne |
| 12 à 14 | veille | Reste dans Inbox « En veille » ; visible dans le pipeline du mardi et du vendredi ; pas de brief |
| 0 à 11 | no_go | Inbox « Écartée », raison écrite ; rien ne va au CRM |
| toute note | dossier_ouvert | Un dossier est déjà ouvert chez cette entreprise : verdict rendu, note calculée, mais Scribe ne crée rien et écrit l'avertissement |

Un doute exprimé par Hugo (annonce incomplète, deux notes possibles) fait descendre au seuil inférieur et
s'écrit dans le détail.

**Plafonds de verdict** (calculés par `pipeline/verdicts.py`, la note n'est jamais modifiée, R7) : un verdict
go_prioritaire devient **veille** quand le titre est senior avec 5 ans et plus demandés (R13), quand le poste est hors
opérations (R14) ou quand le texte est partiel (R15). La ligne reste visible dans le pipeline du mardi et du
vendredi : Tom décide. Commande : `python3 -m pipeline.cli verdict 16 --titre "Senior Revenue Ops" --annees 5`.

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

- **R10 (07/09/2026, précision de Tom)** : **périmètre = tout ce qui touche aux opérations, de 0 à 5 ans**
  demandés, Customer Success Manager inclus au même titre que RevOps et Sales Ops. Les bandes coeur / stretch
  restent affichées mais ne trient plus : les deux passent.

- **R11 (07/09/2026, calibration de Tom)** : **l'entreprise fait la note.** Mot de Tom : « les top postes sont
  dans les opérations d'une scale-up ou d'un grand groupe, même si le poste est plus junior ou sans télétravail ;
  Dust c'est top ». Scale-up financée ou grand groupe privé = C 4/4 d'office ; le type se prouve par
  `rules/entreprises.md` (faits publics sourcés : effectif, levée, label) ou par l'annonce ; entreprise absente du
  registre : une recherche web unique, source citée dans le détail, sinon 0 et « entreprise à qualifier » dans le
  résumé du run. Remplace les quatre sous-points de C (la note Glassdoor n'était citée par aucune annonce).
- **R12 (07/09/2026)** : **ni l'absence de télétravail ni l'absence de salaire ne pénalisent.** B = CDI + lieu +
  salaire non contredit. Résout la contradiction de l'ancien B3 (« fourchette de marché plausible » contre « on
  n'estime jamais »).
- **R13 (07/09/2026)** : **titre senior (Senior, Lead, Head, Director) avec 5 ans et plus demandés = au mieux
  veille.** Note calculée, jamais de brief. Alan Senior Revenue Ops : agent 15, Tom 13 « pas assez d'expérience » ;
  Mistral Enablement Lead (5 à 8 ans) : Tom 14 « un peu junior ». Un « Senior » sans années écrites n'est pas
  plafonné (Cegid : Tom a dit oui).
- **R14 (07/09/2026)** : **hors opérations = au mieux veille** : produit (PM, PO), ingénierie, conseil IA, business
  analyst IA, data. Tom a dit non à 13/20 ou moins à Bpifrance (PM), CNAM (BA IA), Thales (PO), DFM (consultant),
  même en grand groupe. Lu dans le titre seulement, par le code.
- **R15 (07/09/2026)** : **texte partiel** : A plafonné à 6/10 (une couverture ne se mesure pas sur un titre), B et
  C sur les faits publics, verdict au mieux veille (Camille ne briefe pas sans l'annonce). Thales, DFM, Esri,
  ElevenLabs : agent 7 à 9, Tom 10 à 11.
- **R16 (07/09/2026)** : **exclusions lisibles par le code** : `pipeline/exclusions.py` cite la phrase qui exige un
  diplôme d'ingénieur ou d'informatique sans alternative commerce, ou du code au coeur du poste ; Léa l'appelle avant
  de retenir. Meilleurtaux (« Bac +5 École d'Ingénieurs ou Master Informatique ») avait été noté au lieu d'être écarté.

## 7. Calibration du 07/09/2026 (20 offres, notes de Tom contre notes de l'agent)

Tom a noté les 20 offres sur l'artefact « Calibration Léa ». Écart moyen absolu avant les règles R11 à R16 :
**2,1 points** (l'agent notait plus bas, 1,6 point en moyenne) ; après recalcul avec les mêmes tableaux de
couverture : **1,4 point**, objectif ≤ 1,5 atteint. Accord de verdict : les huit offres que l'agent recalculé met à
15 et plus sans plafond (Pennylane, Alan Compliance Ops, ILLUIN, Mirakl, Veepee, Moments Lab, Cegid, Sorare) sont
toutes des « oui » de Tom ; aucun « non » de Tom n'est en go. Détail par offre dans
`data/runs/2026-09-07_test/calibration_tom_vs_agent.md`.

Ce que Tom a dit et qui a produit les règles : « 15/20 car je suis un peu junior » (Pennylane), « le secteur, si
c'est scale-up c'est tous les points » (Alan Compliance Ops, 18), « pas Salesforce mais sinon le poste et
l'entreprise sont top » (Mirakl, 17), « pas assez d'expérience » (Alan Senior, non), « profil trop ingénieur »
(Meilleurtaux, non).
