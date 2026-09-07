# Journal des incidents (à tenir à chaque run qui casse)

| Date | Agent | Symptôme | Cause | Règle ou correctif | Où |
|---|---|---|---|---|---|
| 2026-08-05 | veille v1 | offres pertinentes jamais remontées | filtre hérité trop strict | auditer les rejets, pas seulement les acceptés | `docs/zero-perte.md` |
| 2026-08-10 | notation v1 | note moyenne qui monte chaque semaine | pas de règle d'arbitrage | hésitation = note basse | `rules/criteres.md` § 3 |
| 2026-08-14 | sync v1 | taux de réponse flatteur | accusés automatiques comptés comme réponses | accusé ≠ premier retour | `rules/statuts.md` |
| 2026-08-17 | sync v2 | refus Alan raté | requête FR unique | double requête + réconciliation par dossier | `prompts/05_noe_controle.md` |
| 2026-08-20 | veille v1 | deux fiches Dust le même jour | deux tâches à la même minute, anti-doublon sur URL | clé métier, horaires décalés, Inbox tampon | `pipeline/keys.py` |
| 2026-08-25 | sync v2 | refus Kolecto raté | idem 17/08 | idem | idem |
| 2026-09-02 | audit | 33 fiches sans score, 13 doublons | pas de schéma, dédup sur URL | `crm_row.json`, `dedup.py` | `schemas/` |
| 2026-09-02 | sync v3 | fiches Rivalis, Thoo Owen hors périmètre | création libre depuis Gmail | Noé propose, Tom valide | `prompts/05_noe_controle.md` |
| 2026-09-06 | skill Dust | « pas de malus » et « malus −4 » dans la même skill | correction écrite par-dessus l'ancienne règle | registre numéroté, abrogation explicite (R7) | `rules/criteres.md` § 6 |
| 2026-09-07 | hygiène v3 | 3 nouveaux doublons (Kolecto, Pennylane, Rothschild) sur l'export réel | l'ancienne veille tourne encore sans clé | Scribe les tague ; bascule après calibration | `out/hygiene_2026-09-07.md` |
