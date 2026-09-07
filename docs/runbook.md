# Runbook : faire tourner, réparer, arrêter

## Faire tourner à la main un agent
Ouvrir une conversation Claude (avec les connecteurs Notion et Gmail), coller le prompt de `prompts/` précédé du
protocole commun, et écrire « Exécute ton run maintenant, mode <calibration|production|test> ». En mode `test`,
l'agent ne doit rien écrire : il montre ce qu'il aurait écrit.

## Lire l'état du système en 30 secondes
1. Base **Runs** triée par Horodatage : un run par agent planifié, Statut run = OK.
2. Base **Inbox offres** groupée par Étape : rien en « À noter », « À briefer », « Briefée » de plus de 24 h.
3. Le dernier email « Candidatures, point du soir » : section Hygiène, 0 bloquant.

## Arrêter tout
Paramètres système › Mode = `pause`. Les agents lisent ce paramètre en premier et n'écrivent rien.

## Réparer
| Symptôme | Cause probable | Geste |
|---|---|---|
| `run_manquant` pour un agent | tâche planifiée désactivée, connecteur en erreur, dépôt inaccessible | ouvrir la tâche, lire son dernier run ; relancer à la main |
| `inbox_bloquee` « À noter » | Hugo n'a pas tourné, ou a mis la ligne en Erreur | relancer Hugo ; lire Raison |
| ligne Inbox « Erreur » | schéma refusé (valeur hors liste, champ manquant) | lire Raison ; corriger la donnée à la main ou laisser Léa la re-sourcer demain |
| doublon dans le CRM | fiche créée par Tom ou par l'ancienne tâche sans clé | Scribe la tague 🗑️ au run suivant ; sinon `python -m pipeline.cli hygiene` et corriger |
| offre morte envoyée dans l'email du matin | lien non ATS, page trompeuse | ajouter le motif de fermeture à `DEAD_PATTERNS` dans `link_check.py`, test, commit |
| refus non détecté | formulation hors lexique | ajouter la formule à `REJECT_FR` / `REJECT_EN`, test, commit |
| Noé propose une fiche hors périmètre | filtre de périmètre | ajouter la règle à `rules/statuts.md` § Périmètre |

## Modifier une règle
1. Éditer `rules/criteres.md` (ou `statuts.md`, `sources.md`, `cv.md`) : ajouter une ligne numérotée et datée au registre.
2. `python -m pytest` (les règles codées ont des tests ; une règle de prompt n'en a pas, dis-le dans le commit).
3. Commit, push. Les agents clonent à chaque run : la règle s'applique au run suivant.

## Changer un horaire
Les tâches sont en cron UTC. Paris = UTC+2 jusqu'au 25/10/2026, puis UTC+1 : **décaler d'une heure les crons au
changement d'heure** (ou accepter une heure de dérive).

## Passer sur Dust
`docs/migration-dust.md` : mêmes bases, mêmes règles (en skills), mêmes scripts (Computer ou externes).
