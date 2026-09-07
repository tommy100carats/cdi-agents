# cdi-agents — un pipeline d'agents pour une recherche de CDI, tenu comme un pipeline commercial

Six agents, deux routines, trois bases Notion, du code pour tout ce qu'une règle peut trancher.
Construit par Tom Antonietti pour sa propre recherche de poste RevOps / Sales Ops / AI Ops. Version 3 du
07/09/2026 : remplace la v1 (trois tâches planifiées, un prompt pour trois rôles, 47 jours en production, audit à
10/20) par une chaîne où chaque offre traverse des étapes visibles et où rien ne se perd.

```
Léa (sourcing) → Hugo (notation, sans malus) → Camille (brief PDF) → Scribe (CRM + hygiène)
                                   ↓ Inbox offres (Notion) : une ligne par offre vue, quelle que soit la décision
Noé (contrôle du soir : Gmail → statuts, complétude, relances, PDF)   ·   Inès (CV ciblé, à la demande)
Routine du matin (offres non postulées, liens revérifiés)   ·   Routine pipeline (mardi, vendredi, PDF)
```

## Ce qui est décidé par du code (et testé)

| Quoi | Module | Tests |
|---|---|---|
| Clé métier entreprise + poste (anti-doublon) | `pipeline/keys.py`, `pipeline/dedup.py` | 6 + 7 |
| Séniorité demandée (≤ 3 ans coeur, 3–5 stretch, > 5 hors) | `pipeline/seniority.py` | 4 |
| Offre encore active (API Ashby / Greenhouse / Lever, HTTP, illisible = inconnu) | `pipeline/link_check.py` | 6 |
| Validité de chaque écriture (JSON Schema) | `schemas/*.json`, `pipeline/validate.py` | 3 |
| Classement d'un email de recrutement, précédence des statuts, relances | `pipeline/precedence.py`, `pipeline/relances.py` | 10 |
| Hygiène de la base (9 familles de contrôles) et rapports PDF | `pipeline/hygiene.py`, `pipeline/report.py` | 4 |
| CV : 14 contrôles sur les données, 2 sur le PDF, diff contre la référence | `cv/cv_check.py`, `cv/cv_diff.py` | constaté sur un CV réel |

`python -m pytest` : 37 tests, dont plusieurs sur l'export réel du CRM (213 lignes, 07/09/2026).

## Démarrer

```bash
git clone https://github.com/tommy100carats/cdi-agents.git && cd cdi-agents
pip install -r requirements.txt
python -m pytest -q
python -m pipeline.cli hygiene data/crm_export_2026-09-07.json --today 2026-09-07 --md
python -m pipeline.cli report data/crm_export_2026-09-07.json --mode soir --today 2026-09-07 --pdf etat.pdf
```

Les agents sont des tâches planifiées Claude (connecteurs Notion et Gmail) dont les prompts sont dans
`prompts/`, précédés de `prompts/_protocole_commun.md`. Chaque run clone ce dépôt, lit `rules/`, exporte les
bases en JSON, fait valider ses écritures par `pipeline/cli.py`, puis écrit une ligne dans la base Runs.

## Lire dans l'ordre

1. `docs/architecture.md` : la chaîne, les bases, les effets de bord de chaque agent.
2. `docs/determinisme.md` : la frontière code / modèle, et comment on sait que le modèle passe par le code.
3. `docs/zero-perte.md` : où chaque donnée vit, les trous de la v1 et leurs bouchons.
4. `docs/calibration.md` : les 20 offres, les corrections de notation, le registre.
5. `docs/grille-18-20.md` : l'auto-évaluation face à deux RevOps seniors, et ce qui manque.
6. `docs/runbook.md`, `docs/incidents.md`, `docs/migration-dust.md`.

## Règles (source de vérité, lues par les agents à chaque run)

`rules/criteres.md` (périmètre, grille v3 additive sans malus, registre R1–R9), `rules/statuts.md`,
`rules/sources.md` (où chercher, API d'ATS, slugs), `rules/profil.md` (faits et chiffres autorisés), `rules/cv.md`.

## Ce que ce dépôt ne fait pas

Il ne candidate pas, n'écrit à aucun recruteur, ne supprime rien, n'estime rien. Il ne lit ni LinkedIn ni
Welcome to the Jungle (pages illisibles par du code : ces offres vont en veille jusqu'à un lien vérifiable).
Il n'a pas encore tourné un jour complet en production : voir `docs/grille-18-20.md` pour ce que ça change.
