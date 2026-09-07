# Règles de rédaction des CV et lettres (v3, 07/09/2026)

Source complète : `claude/regles-redaction-cv.md` (projet Claude). Ce qui est vérifié par `cv/cv_check.py` est marqué ⚙️.

## Structure figée
- Générateur `cv/cv_build.py`, deux colonnes, une page ⚙️. La maquette ne change jamais ; le contenu, oui.
- Bandeau : nom, titre reprenant l'intitulé de l'annonce, contacts (« Paris · Permis B », GitHub).
- Colonne gauche : Formation, Compétences clés (ordre = ordre des responsabilités de l'annonce), Outils,
  Langues, Certifications, Centres d'intérêt (bloc témoin ⚙️).
- Colonne droite : Profil (4 à 6 lignes ⚙️), Expériences (chronologie inverse ⚙️), Projets personnels.

## Accroche
- « emlyon business school » en minuscules ⚙️ ; entreprise cible nommée ⚙️ ; « Disponible immédiatement » en fin ⚙️ ;
  aucune langue dans le profil ⚙️.
- Ouverture par défaut : observer, échanger, lire ; simplifier, outiller, automatiser ; mesurer. Ouverture
  « bâtisseur » seulement si l'annonce parle de zero-to-one. En français, jamais « zero to one » ⚙️.

## Zéro invention
- Chiffres : uniquement ceux de `rules/profil.md` (whitelist ⚙️). « 3 M€ » est le CA du centre sous responsabilité,
  jamais « généré par moi ». Le partenaire du process en 23 étapes n'est jamais nommé.
- Outils : HubSpot (certifié), Salesforce (notions) ⚙️ ; aucun langage de programmation ⚙️ ; SQL hors certification
  déclenche un avertissement ⚙️ (invite un test live).
- Agents IA : bloc Projets personnels uniquement, jamais dans une puce salariée ⚙️ ; « tournent sur Claude,
  Notion, Dust », jamais « built on n8n » ⚙️ ; « validation humaine avant toute action irréversible », jamais
  « avant toute écriture » ⚙️.
- Traits de caractère : aucun qui ne soit prouvable par trois exemples en entretien (« I like documenting » interdit ⚙️).

## Style
- Aucun tiret long ⚙️ ; pas de placeholder `{{` ⚙️ ; nom de fichier avec espaces, sans underscore ⚙️.
- Mentalizi : quand le secteur s'y prête ou que l'annonce demande un side project no-code / IA.
- IA : pas un mot si l'annonce ne l'appelle pas ; une mention si elle est AI-first.

## Avant envoi
`python3 cv/cv_diff.py` (ne relire que le diff) puis `python3 cv/cv_check.py <fichier> --build` à 0 FAIL, puis Tom lit le PDF.
