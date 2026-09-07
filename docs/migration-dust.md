# Migration vers Dust (après calibration)

Le tuto détaillé (agents, skills, tools, stakes, triggers, structured output) est dans le projet Claude
(`claude/tuto-migration-dust.md`). Ce qui change avec la v3 :

- **Inbox offres reste la zone de transit** : chaque agent Dust a un trigger et lit / écrit sa propre Étape via
  le tool Notion. Pas besoin de Run agent pour enchaîner : la base est la file d'attente.
- **Les règles deviennent des skills** : `rules/criteres.md` → skill « Critères de recherche » ; `rules/statuts.md`
  → « Statuts & lexique » ; `rules/cv.md` → « Règles CV ». Le registre reste dans le dépôt et se recopie dans la
  skill à chaque commit (source de vérité : le dépôt).
- **Les scripts** : soit la skill Computer de Dust (clone du dépôt, `pip install`, mêmes commandes), soit exécution
  externe ; dans les deux cas les mêmes fichiers JSON et les mêmes schémas.
- **Structured output** : `schemas/verdict.json`, `brief.json`, `offre.json` se collent tels quels dans
  Advanced › Structured Response Format des agents Hugo, Camille, Léa.
- **Stakes** : Notion insert row = Low (Léa, Scribe), update property = Low (Noé), create page depuis Gmail =
  High (Noé), Gmail send_mail = Medium sur Email Tom (routines).
- **Calibration** : identique, sur les mêmes 20 lignes Inbox.
