# IA pour optimiser l'action humanitaire sur le terrain

Ce module propose une base **opérationnelle et éthique** pour aider des équipes humanitaires à:

1. prioriser les zones d'intervention,
2. allouer les ressources (kits, équipes, véhicules),
3. planifier les tournées terrain,
4. suivre l'impact en continu.

## Principes clés

- **Human-in-the-loop**: l'IA recommande, les décideurs valident.
- **Transparence**: chaque recommandation est expliquée.
- **Sécurité**: minimisation des données personnelles et audit des décisions.
- **Robustesse terrain**: fonctionnement possible avec données incomplètes.

## Architecture recommandée

```text
Collecte (ONG, satellites, météo, santé, logistique)
    -> Validation qualité
    -> Modèle de scoring multi-critères
    -> Optimisation allocation & itinéraires
    -> Tableau de bord décisionnel
```

## Démarrage rapide

```bash
python humanitarian_ai/prioritization.py
```

Le script affiche une priorisation simple des zones et une allocation heuristique des kits.

## Variables de score (exemple)

- population affectée
- sévérité sanitaire
- difficulté d'accès
- niveau de vulnérabilité
- stock local disponible

Le score est configurable selon le contexte (conflit, inondation, épidémie, etc.).

## Plan de déploiement (90 jours)

- **S1-S2**: cadrage, gouvernance des données, KPI, protocole éthique.
- **S3-S6**: MVP scoring + dashboard + pilote terrain sur 1 zone.
- **S7-S10**: ajout optimisation logistique et mécanisme de feedback.
- **S11-S13**: audit biais, sécurité, montée en charge multi-zones.

## KPI recommandés

- temps moyen de réponse,
- couverture des populations vulnérables,
- taux de ruptures de stock,
- coût logistique par bénéficiaire,
- écart entre recommandation IA et décision finale (pour apprentissage).
