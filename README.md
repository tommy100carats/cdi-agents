# cdi-agents : un pipeline d'agents IA pour une recherche de CDI, tenu comme un pipeline commercial

Six agents, deux routines, trois bases Notion, et du code pour tout ce qu'une règle peut trancher.
Conçu et piloté par Tom Antonietti pour sa propre recherche de poste en opérations commerciales.
**En production quotidienne depuis mi-septembre 2026.**

```
Léa (sourcing) → Hugo (notation) → Camille (brief PDF) → Scribe (CRM + hygiène)
                       ↓ Inbox offres (Notion) : une ligne par offre vue, quelle que soit la décision
Noé (contrôle du soir : Gmail → statuts, complétude, relances)   ·   Inès (CV ciblé, à la demande)
Routine du matin (offres non postulées, liens revérifiés)   ·   Routine pipeline (mardi et vendredi)
```

## Une journée type

Chiffres du point du soir du 01/10/2026, tels que le système les calcule : Léa a analysé **69 annonces**, en a
remonté **19** à Hugo, qui les a toutes notées, dont **14 à 13/20 ou plus** versées au CRM. Les écarts sont
motivés et comptés (séniorité, contrat, exclusion technique, géographie). Le contrôle du soir réconcilie le CRM
avec Gmail, signale les relances dues et vérifie que rien n'est passé à la trappe (0 offre bloquée, 0 run manquant).

## Le principe : le modèle propose, le code tranche

Tout ce qu'une règle peut décider est décidé par du code testé, jamais par le modèle :

| Quoi | Module |
|---|---|
| Clé métier entreprise + poste (anti-doublon) | `pipeline/keys.py`, `pipeline/dedup.py` |
| Séniorité demandée par l'annonce | `pipeline/seniority.py` |
| Verdict à partir de la note, plafonds compris | `pipeline/verdicts.py` |
| Offre encore active (API Ashby, Greenhouse, Lever ; illisible = inconnu) | `pipeline/link_check.py` |
| Validité de chaque écriture (JSON Schema) | `schemas/*.json`, `pipeline/validate.py` |
| Classement d'un email de recrutement, précédence des statuts, relances | `pipeline/precedence.py`, `pipeline/relances.py` |
| Hygiène de la base (9 familles de contrôles) et rapports | `pipeline/hygiene.py`, `pipeline/report.py` |
| CV : 14 contrôles sur les données, 2 sur le PDF | `cv/cv_check.py` |

**69 tests** (`python -m pytest`), exécutés par la CI à chaque push.

## Garde-fous

- **Effets de bord déclarés** : chaque agent a la liste écrite de ce qu'il a le droit de modifier (`docs/architecture.md`).
- **Fail-closed** : si le dépôt, Notion ou un schéma manque, l'agent s'arrête sans écrire et le dit.
- **Zéro invention** : un chiffre absent de `rules/profil.md` est interdit ; une donnée manquante reste vide.
- **Décision humaine** : le système ne candidate pas, n'envoie aucun message (les relances restent en brouillon) et ne supprime rien.
- **Journal** : chaque run écrit une ligne dans une base Runs ; les incidents sont tenus dans `docs/incidents.md`.

## Comment il est construit

Je conçois l'architecture, j'écris les règles et je valide chaque comportement. Le code est écrit par des agents
de code (Claude Code) sous ma supervision, ce qui explique les commits signés « Claude ». Les agents sont des
tâches planifiées Claude connectées à Notion et Gmail ; leurs prompts sont dans `prompts/`. Chaque run clone ce
dépôt, lit `rules/`, exporte les bases en JSON, fait valider ses écritures par `pipeline/cli.py`, puis journalise.

## Essayer

```bash
git clone https://github.com/tommy100carats/cdi-agents.git && cd cdi-agents
pip install -r requirements.txt
python -m pytest -q
python -m pipeline.cli hygiene data/crm_export_2026-09-07.json --today 2026-09-07 --md
```

Les données d'exemple (`data/`) sont un export réel du CRM **anonymisé** : entreprises remplacées par
« Entreprise NNN », liens et notes retirés. Les réglages personnels (seuils, identifiants) vivent dans une base
Notion privée, pas dans ce dépôt.

## Lire dans l'ordre

1. `docs/architecture.md` : la chaîne, les bases, les effets de bord de chaque agent.
2. `docs/determinisme.md` : la frontière entre code et modèle.
3. `docs/zero-perte.md` : où chaque donnée vit, et comment rien ne se perd.
4. `docs/calibration.md` : comment la notation a été calée sur 20 offres notées à la main (écart moyen 2,1 puis 1,4).
5. `docs/runbook.md`, `docs/incidents.md`.

Règles lues par les agents à chaque run : `rules/criteres.md` (périmètre, grille additive, registre daté des
corrections), `rules/entreprises.md`, `rules/statuts.md`, `rules/sources.md`, `rules/profil.md`, `rules/cv.md`.

## Limites connues

Le système ne lit pas LinkedIn ni Welcome to the Jungle par du code : ces offres passent avec « Non vérifiable »
et ne sont jamais présentées comme actives. Le rapport PDF du soir ne part pas encore en pièce jointe (le mail HTML
fait foi).
