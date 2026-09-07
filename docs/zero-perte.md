# Zéro perte de données : où chaque information vit, et comment on sait qu'elle n'a pas disparu

## Le contrat

Toute donnée qui entre dans le système laisse une trace **avant** qu'un agent la juge. On ne trie pas dans
la tête du modèle ; on trie dans une base, avec un motif.

| Entrée | Trace obligatoire | Qui vérifie |
|---|---|---|
| Une offre vue par Léa (alerte, ATS, web) | ligne Inbox, quelle que soit la décision : À noter, En veille, Écartée (raison), Doublon (lien de l'original), Erreur (message du validateur) | Noé : `inbox_bloquee`, `run_manquant` ; Runs : Lues = Écrites + Écartées + Erreurs (sinon Partiel) |
| Une note de Hugo | champs Score agent, Verdict, Détail notation sur la ligne Inbox | Noé : lignes « À noter » de plus de 24 h |
| Un brief de Camille | Brief et Brief PDF sur la ligne Inbox, contenu de la fiche CRM | Noé : lignes « À briefer » de plus de 24 h |
| Une fiche CRM | créée uniquement depuis « Briefée », avec `Lien Inbox` et `Clé` ; la ligne Inbox porte `Lien CRM` | hygiène : `doublon_cle`, `score_manquant`, `lien_absent` |
| Un email de recrutement | objet `evenement_gmail` validé ; note datée « 📅 MAJ » ou « REFUS reçu » sur la fiche ; les cas inconnus dans la section « À valider par Tom » de l'email du soir | Noé : réconciliation par dossier ouvert, sur 10 jours |
| Un run d'agent | ligne Runs, même en échec, avec la sortie brute des scripts | Noé : `run_manquant` |
| Une correction de Tom (décision, score, commentaire) | champs Décision Tom, Score Tom, Commentaire Tom sur la ligne Inbox ; règle numérotée dans `rules/criteres.md` | revue de calibration |

## Les trous connus de la v1, et le bouchon v3

| Trou v1 | Cause | Bouchon v3 |
|---|---|---|
| Offres pertinentes jamais vues | filtre trop strict dans un seul prompt ; les rejets n'étaient écrits nulle part | tout rejet est une ligne Inbox « Écartée » avec raison ; audit des rejets possible |
| 33 fiches sans score | pas de schéma | `crm_row.json` exige un entier 0–20 ; Notion refuse une chaîne |
| 13 doublons | anti-doublon sur l'URL | clé métier calculée par code, vérifiée contre CRM et Inbox, y compris dans le lot du jour |
| Refus Alan, Kolecto ratés ; candidature Numberly manquée | une seule requête Gmail en français | deux requêtes + réconciliation par dossier ouvert + lexique FR/EN en code |
| Fiches créées hors périmètre (Rivalis, Thoo Owen) | création libre depuis Gmail | Noé ne crée jamais ; il propose, Tom valide |
| Champs « Effectif » et « Cold call » écrits dans le vide | le prompt écrivait des propriétés qui n'existaient pas dans la base | schéma aligné sur la base ; `Effectif` créé ; propriétés inconnues refusées par `additionalProperties: false` |
| Deux tâches à la même minute sur la même base | crons identiques | horaires décalés, un agent par étape, Inbox comme tampon |
| « Comment tu sais que ça marche ? » | rien | base Runs + hygiène quotidienne + rapport du soir |

## Pannes prévues

- **Notion indisponible** : l'agent s'arrête sans écrire ; pas de ligne Runs possible ; le trou est visible le
  lendemain (`run_manquant`) et la fenêtre de 4 jours de Noé rattrape les emails.
- **Gmail indisponible** : Léa continue sans les alertes (le dit) ; Noé s'arrête, ligne Runs « Échec ».
- **Dépôt de code inaccessible** : aucun agent n'écrit (fail-closed).
- **Site d'annonce illisible** (LinkedIn, WTTJ) : « Non vérifiable », l'offre passe, texte partiel signalé, jamais présentée comme active.
- **Un agent dépasse son budget** : « Partiel » dans Runs, les lignes restent à leur étape, le run suivant reprend.
- **Deux runs d'un même agent le même jour** (relance manuelle) : idempotence par clé, par Étape, par note datée.

## Ce que Tom doit faire à la main, et où c'est écrit

Postuler ; répondre à un recruteur ; valider une fiche proposée par Noé ; fermer une candidature silencieuse ;
décider en calibration ; faire entrer une correction au registre par un commit. Tout le reste est automatique,
réversible, borné et tracé.
