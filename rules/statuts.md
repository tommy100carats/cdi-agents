# Statuts, précédence, lexique — v3 (07/09/2026)

Appliqué par `pipeline/precedence.py` (code) et lu par Noé et Scribe. Le modèle propose un événement ;
le code décide du statut.

## Étapes de l'Inbox (chaîne du matin)

`Sourcée` → `À noter` (lien vérifié, périmètre OK) ou `Écartée` (raison) ou `Doublon` (lien vers l'original)
→ `Notée` → `À briefer` (note ≥ seuil CRM) ou `En veille` (entre seuil veille et seuil CRM) ou `Écartée`
→ `Briefée` → `Transférée` (fiche CRM créée, `Lien CRM` renseigné). `Calibration` : lignes proposées à Tom
pour décision. `Erreur` : un script a refusé l'écriture, raison dans `Raison`.

Une ligne Inbox ne se supprime jamais. Une ligne bloquée plus de 24 h à une étape intermédiaire est un
incident détecté par Noé (`inbox_bloquee`).

## Statuts du CRM (options exactes)

`À contacter` < `Candidature envoyée` < `Entretien` < `Test / Étude de cas` < `Offre reçue` < `Accepté`.
`Refusé / Clos` peut succéder à n'importe quel statut. `En veille` n'est pas un rang : c'est l'état de
l'incertitude, toujours avec un motif daté dans Notes.

## Précédence

- Le statut monte, **jamais ne recule**.
- Un dossier `Refusé / Clos` ne se rouvre jamais automatiquement (réouverture manuelle par Tom).
- Une fiche `En veille` est réveillée par une vraie interaction de recrutement.
- **Un doute exprimé bloque la progression** : le doute s'écrit dans Notes, le statut ne change pas.

## Événements Gmail → statut

| Événement | Preuve requise | Statut | Prochaine relance |
|---|---|---|---|
| accusé de réception | « bien reçu », « we received », « thank you for applying »… | Candidature envoyée (+ Date candidature si vide) | J+10 |
| créneau proposé | « book a slot », « réserver un créneau », lien Calendly… | **inchangé**, note « créneau proposé le JJ/MM » | J+1 |
| entretien confirmé | invitation d'agenda, ou confirmation avec **date et heure** | Entretien | J+2 |
| test / étude de cas | « case study », « take-home », « exercice »… | Test / Étude de cas | J+3 |
| offre | « offer letter », « proposition d'embauche »… | Offre reçue | J+1 |
| refus | lexique ci-dessous | Refusé / Clos, Notes « REFUS reçu le JJ/MM (auto Gmail) : citation, expéditeur » | ne pas toucher |
| inconnu | — | inchangé, listé « à relire » | — |

Un accusé automatique n'est **jamais** présenté comme un premier retour humain.

## Lexique de refus

FR : ne pas donner suite · ne donnerons pas suite · pas donner une suite favorable · n'a pas été retenue ·
pas retenu · malheureusement · nous avons décidé de ne pas · d'autres candidats · plus proches des exigences ·
nous ne poursuivrons pas · ne correspond pas · pas été sélectionné.
EN : unfortunately · not be progressing · will not be moving forward · not moving forward · decided not to ·
other candidates · more closely match · regret to inform · we won't be · not the right fit at this time ·
decided to pursue other · not selected.

## Périmètre d'une fiche

Une fiche concerne un CDI, dans une famille de `rules/criteres.md`, chez un employeur identifiable par un
domaine professionnel. Une approche par Gmail personnel, une mission, une franchise : hors périmètre, aucune
fiche créée, signalé dans le résumé. **Créer une fiche CRM depuis Gmail est une action à validation humaine**
(Noé propose, Tom clique).

## Relances (voir `pipeline/relances.py`)

Candidature sans retour humain : J+10 puis J+20 ; sans réponse à J+21, elle **compte comme un refus dans les
statistiques** (elle reste ouverte dans le CRM tant que Tom ne la ferme pas). Entretien tenu : remerciement
J+1 / J+2, relance J+7. Offre : réponse sous 48 h. La date `Prochaine relance` du CRM prime sur ces défauts.

## Clé métier

Avant toute création, interroger la propriété `Clé` (égalité stricte, calculée par `pipeline/keys.py`). Une
ligne existante pour le même couple entreprise + poste, quel que soit son statut, se met à jour ; on ne crée
jamais une seconde fiche. Un refus clôt le dossier et libère l'entreprise pour un autre poste ; le même poste
reste bloqué 365 jours dans certains ATS (constaté chez Alan).
