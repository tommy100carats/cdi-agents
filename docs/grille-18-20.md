# La grille des deux RevOps seniors : objectif 18/20

*Ce que deux RevOps expérimentés regarderaient s'ils évaluaient ce système comme un pipeline qu'on leur
demande de reprendre. Dix critères, deux points chacun. Auto-évaluation honnête au 07/09/2026, avant le
premier run réel, puis ce qui manque pour 18.*

| # | Critère | Ce qu'un senior attend | État au 07/09 | /2 |
|---|---|---|---|---|
| 1 | **Modèle de données** | Étapes explicites, clé métier, propriétaire de chaque champ, aucune propriété écrite dans le vide | Inbox avec Étape, Clé calculée, `Écrit par` / `Run` sur chaque ligne, schémas alignés sur les bases, `Effectif` créé | 2 |
| 2 | **Discipline des étapes** | Un statut ne recule pas ; une étape exige une preuve ; les exceptions sont nommées | `precedence.py` : monotone, « Entretien » exige date et heure, doute = blocage, En veille avec motif | 2 |
| 3 | **Dédoublonnage** | Sur une clé métier, pas sur un identifiant technique ; alias d'employeurs | `keys.py` + `dedup.py`, alias, testé sur l'export réel (3 nouveaux doublons trouvés le 07/09) | 2 |
| 4 | **SLA et relances** | Règles de relance écrites, dues calculées, silence traité comme un refus dans les stats | `relances.py`, J+10 / J+2 / J+1 / J+3, 21 jours = refus statistique, listées chaque soir | 2 |
| 5 | **Observabilité** | Journal des runs, contrôle quotidien, alertes sur trou de données | Base Runs, `hygiene.py` (9 familles de contrôles), `inbox_bloquee`, `run_manquant`, rapport du soir | 1,5 : pas encore un jour de runs réels |
| 6 | **Portes humaines** | Rien d'irréversible sans humain ; le reste automatique, réversible, tracé | Jamais de suppression ; création depuis Gmail = proposition ; candidater = Tom ; un seul destinataire d'email | 2 |
| 7 | **Mesure et KPI** | Entonnoir, conversion, activité de la semaine, un seul jeu de chiffres | `report.py` : quatre indicateurs, entonnoir, semaine ; encore aucune baseline chronométrée | 1,5 |
| 8 | **Boucle de calibration** | Le scoring se corrige sur des cas, avec un registre, pas à l'intuition | Protocole 20 offres, registre R1–R9, seuils de validation (70 %, écart ≤ 1,5) | 1,5 : pas encore exécuté |
| 9 | **Documentation et reprise** | Un nouveau venu peut faire tourner et modifier le système sans l'auteur | README, architecture, déterminisme, zéro perte, runbook, prompts versionnés, 37 tests, CI | 2 |
| 10 | **Coût et limites** | Ce que ça coûte, ce que ça ne fait pas, ce qui reste manuel | Limites écrites (pages illisibles, lexique, pas de baseline) ; coût des tâches Claude non chiffré | 1 |

**Auto-évaluation : 17,5 / 20 sur le papier ; 15 / 20 tant que la calibration et trois jours de runs réels
n'ont pas eu lieu.** Les deux points qui manquent ne s'écrivent pas, ils se constatent :

1. **Sept jours de Runs sans `run_manquant` ni `inbox_bloquee`** (critères 5 et 7) : c'est ce qui transforme
   l'observabilité annoncée en observabilité prouvée. Livrable : la capture de la base Runs et le rapport du
   septième soir.
2. **La calibration terminée** (critère 8) : 20 décisions de Tom, écart moyen ≤ 1,5, registre à R12 ou plus.
   Livrable : la vue « Calibration » de l'Inbox et le diff de `rules/criteres.md`.
3. **Une baseline** (critère 7) : chronométrer trois qualifications manuelles (sourcer, vérifier, noter, briefer)
   pour donner un chiffre honnête au « temps gagné ».
4. **Le coût** (critère 10) : nombre de runs par semaine × durée moyenne, lu dans Runs ; à chiffrer après une
   semaine.

Un senior ne donnera pas 18 à un système qui n'a pas tourné. Il le donnera à un système qui a tourné, a cassé,
et dont les cassures sont dans le journal avec la règle qui en est sortie. C'est la raison d'être de
`docs/incidents.md`, à alimenter dès le premier run.
