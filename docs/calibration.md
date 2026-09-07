# Calibration : les 20 offres, puis les corrections de notation

*Avant de valider les agents, on les fait travailler sous contrôle : Léa propose 20 offres, Tom dit oui ou non ;
Hugo les note, Tom corrige et explique ; les explications deviennent des règles numérotées. Le système ne
passe en production qu'après.*

## Étape 1 : calibrer le sourcing (Léa)

1. Paramètres › Mode = `calibration` (déjà positionné le 07/09/2026).
2. Léa tourne (planifiée ou lancée à la main) : elle crée exactement **20 lignes Inbox en Étape « Calibration »**,
   avec pour chacune : Bande séniorité, Actif vérifié, Preuve activité, et dans `Raison` la phrase « je pense que
   ça correspond parce que … ». Le contenu de la page est l'annonce intégrale.
3. Tom remplit, ligne par ligne, **Décision Tom** (Oui / Non / Plus tard) et, pour chaque Non, **Commentaire Tom**
   en une phrase (« trop senior », « outbound pur », « pas mon secteur », « lieu KO », « ok mais salaire bas »…).
4. Critère de validation : au moins **14 Oui sur 20** (70 %). En dessous, on lit les Non, on ajoute les règles au
   § 1 de `rules/criteres.md` (périmètre) ou à `rules/sources.md` (sources), et on refait un lot de 20.
5. Les lignes « Calibration » restent dans l'Inbox : c'est le jeu de test de référence du sourcing.

## Étape 2 : calibrer la notation (Hugo)

1. Sur les mêmes 20 lignes, Hugo écrit **Score agent**, **Verdict**, **Détail notation** (tableau de couverture,
   sous-scores A/B/C/D), **Règles appliquées**.
2. Tom remplit **Score Tom** et, quand l'écart avec Score agent dépasse 2 points, **Commentaire Tom** : la raison
   de l'écart (« + grand groupe », « + entreprise ambitieuse, levée en juin », « − ils veulent du Salesforce
   hands-on », « la couverture est trop généreuse sur HubSpot »…).
3. Hugo, au run suivant, lit les commentaires et **propose** des règles au format du registre : constat chiffré,
   règle en une phrase, effet attendu. Il n'écrit rien dans le dépôt.
4. Tom valide les règles qui lui conviennent ; elles entrent dans `rules/criteres.md` § 6 par un commit (R10,
   R11…), datées. Une règle qui n'est pas dans le registre n'existe pas.
5. Critère de validation : **écart moyen absolu ≤ 1,5 point** sur les 20 offres et **aucune inversion de seuil**
   (une offre que Tom met à 15 ou plus et que Hugo met sous 15, ou l'inverse). Sinon, second tour.

**Premier tour, fait le 07/09/2026** : Tom a noté les 20 offres sur l'artefact « Calibration Léa » (notes, oui /
non, commentaires). Écart moyen 2,1 avant, 1,4 après les règles R11 à R16 (`rules/criteres.md` § 6 et § 7,
tableau complet dans `data/runs/2026-09-07_test/calibration_tom_vs_agent.md`). Aucune inversion : les huit offres
à 15 et plus sans plafond sont huit « oui » de Tom. Un écart de 5 subsiste sur Alan Senior Revenue Ops (Tom 13,
agent 18) : la grille n'a pas de malus, le plafond R13 règle le routage (veille, pas de brief), pas le chiffre.
Second tour : sur le prochain lot de 20 offres sourcées en production, comparer Score Tom et Score agent avec la
grille v3.1 ; les règles R17 et suivantes viendront de là.

## Étape 3 : bascule

1. Vérifier que Camille et Scribe produisent, sur 3 lignes « Briefée » de test, des fiches CRM valides
   (`validate crm_row` à 0 erreur, brief PDF présent).
2. Paramètres › Mode = `production`.
3. Trois jours de chaîne complète en parallèle des anciennes tâches Claude (qui écrivent encore dans le CRM
   avec leur ancien prompt). Chaque soir, le rapport de Noé doit montrer : 0 `doublon_cle` créé par la nouvelle
   chaîne, 0 `score_manquant` sur les fiches `Écrit par = Scribe_CRM`, 0 `inbox_bloquee`.
4. Désactiver les anciennes tâches (veille, sync v3, Top 5 v1).

## Tenue du registre

- Une règle = un numéro, une date, un constat, une phrase. Jamais rediscutée sans un nouveau constat.
- Une règle qui contredit une règle précédente l'abroge explicitement (« abrogée par R7 »).
- Le registre vit dans `rules/criteres.md` ; les prompts ne le recopient pas, ils le lisent.

## Mesure continue (après la bascule)

La routine du mardi et du vendredi affiche la distribution des notes et, dès 10 candidatures par tranche, le
taux de réponse humaine par tranche de note. Le taux doit monter avec la note ; s'il baisse, il manque un
critère d'accessibilité et on revient à l'étape 2 avec un nouveau lot.
