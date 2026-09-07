# Déterminisme et contrôle : ce qui est prouvé, et comment

*La question d'un RevOps senior n'est pas « est-ce que ton agent est intelligent » mais « qu'est-ce qui
l'empêche d'écrire n'importe quoi dans mon CRM ». Voici la réponse, ligne par ligne.*

## 1. La frontière

| Décision | Qui décide | Où | Preuve |
|---|---|---|---|
| Deux offres sont-elles la même ? | code | `pipeline/keys.py`, `pipeline/dedup.py` | `tests/test_keys.py`, `tests/test_dedup_hygiene.py` sur l'export réel |
| L'offre demande-t-elle trop d'expérience ? | code | `pipeline/seniority.py` | `tests/test_seniority.py` |
| L'offre est-elle encore active ? | code (API ATS, HTTP) ; « inconnu » si illisible | `pipeline/link_check.py` | `tests/test_link_check.py` (fetch injecté) |
| Cette écriture est-elle valide ? | code (JSON Schema 2020-12) | `schemas/*.json`, `pipeline/validate.py` | `tests/test_validate_report.py` |
| Cet email est-il un refus, un accusé, un entretien ? | code (lexique) | `pipeline/precedence.py` | `tests/test_precedence.py` |
| Le statut peut-il changer ? | code (précédence, jamais de recul, doute = blocage) | `pipeline/precedence.py` | idem |
| Quand relancer ? | code | `pipeline/relances.py` | idem |
| La base est-elle propre ? | code | `pipeline/hygiene.py` | idem, sur l'export réel |
| Le rapport du soir | code | `pipeline/report.py` | idem |
| Le CV respecte-t-il les règles ? | code (16 contrôles) | `cv/cv_check.py` | 5 constats sur un CV réel du 14/08 |
| Lire une annonce, cartographier les exigences, écrire un brief, adapter une accroche | modèle | prompts | relecture humaine des sorties (diff, détail de notation) |

## 2. Comment on s'assure que le modèle passe bien par le code

Un prompt peut être ignoré par un modèle. Quatre mécanismes rendent l'oubli visible ou impossible :

1. **Fail-closed sur le code** : si le dépôt n'est pas cloné, l'agent s'arrête sans écrire (protocole, étape B).
2. **Écriture depuis un fichier validé** : le prompt impose « écris le JSON, valide, puis écris dans Notion à
   partir du JSON validé ». Le champ `Contrôles` de la base Runs doit contenir la sortie du validateur ;
   une ligne Runs sans sortie de script est un incident que Noé remonte.
3. **Le schéma Notion lui-même** : `Score /20` est un nombre, `Statut` une liste fermée, `Étape` une liste
   fermée. Une valeur hors liste est refusée par Notion, pas par le modèle.
4. **Le contrôle du soir** : `hygiene.py` recalcule tout depuis l'export (doublons de clé, scores vides, statuts
   invalides, lignes Inbox bloquées, runs manquants). Ce qui a échappé au matin est vu le soir, et chiffré.

## 3. Ce qui reste probabiliste, et comment on le borne

- **La note** (bloc A de la grille, couverture) dépend de la lecture de l'annonce par le modèle. Bornes :
  tableau de couverture obligatoire (une ligne par exigence, preuve verbatim), hésitation = note basse,
  distribution des notes surveillée par la revue, calibration sur 20 offres avec Tom (`docs/calibration.md`),
  registre des corrections appliqué par numéro.
- **Le classement d'un email** est déterministe mais lexical : un email hors lexique sort « inconnu » avec
  `needs_review = true`, ce qui bloque toute écriture et le met dans la liste « à relire » de Tom. Le
  faux négatif coûte une relecture ; le faux positif est impossible par construction.
- **L'activité d'une page HTML** hors ATS : détection de 404 et de motifs de fermeture. Une page ambiguë sort
  « inconnu » : l'offre passe, marquée « Non vérifiable », jamais présentée comme active.

## 4. Idempotence

- Léa : clé métier vérifiée contre CRM et Inbox avant toute création ; rejouer un run ne crée rien.
- Noé : une note « 📅 MAJ » ou « REFUS reçu » portant la même date ou le même objet bloque la réécriture ;
  fenêtre de 4 jours pour couvrir un run manqué sans double traitement.
- Scribe : une ligne Inbox « Briefée » devient « Transférée » avec le lien de la fiche ; rejouer ne crée
  pas de seconde fiche (dedup par clé, puis Étape).

## 5. Sécurité

- Le seul destinataire d'un email est `Email Tom` (Paramètres). Aucun agent n'a l'instruction d'écrire à un
  recruteur, et le connecteur Gmail n'est pas utilisé en `reply`.
- Aucune suppression, aucune archive : les erreurs vont en « En veille » ou « Erreur » avec motif daté.
- Injection : tout contenu lu (web, email, annonce) est une donnée ; une consigne trouvée dans une annonce est
  signalée et ignorée. Le contrôle du soir détecte une écriture anormale (statut, clé, run).
- Les scripts n'ont pas de clés d'API : ils travaillent sur des exports JSON et des URL publiques. Les accès
  Notion et Gmail passent par les connecteurs de la session, révocables d'un clic.
- Aucune donnée personnelle de tiers n'est stockée hors du CRM (le nom d'un recruteur dans une note, au plus).

## 6. Ce que ce dépôt ne prouve pas

La conformité au prompt d'un run donné ne se vérifie qu'a posteriori (Runs, hygiène). Le passage sur Dust
apporte un cran de plus : des outils avec niveaux d'approbation par action et un structured output imposé
par la plateforme.
