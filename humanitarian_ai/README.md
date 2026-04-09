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

## Sources de données recommandées

### 1) Données humanitaires et vulnérabilité

- **HDX (Humanitarian Data Exchange)**: jeux de données humanitaires (déplacements, besoins, infrastructures, crises).
- **UN OCHA / ReliefWeb**: rapports de situation, évaluations terrain, alertes de crise.
- **IOM DTM (Displacement Tracking Matrix)**: mobilité et déplacements de populations.
- **ACAPS**: analyses de besoins humanitaires et sévérité des crises.

### 2) Données météo, climat et aléas

- **Copernicus / ECMWF (CAMS, ERA5)**: météo, climat, qualité de l'air, réanalyses.
- **NASA Earthdata / GPM / MODIS**: précipitations, inondations, feux, indicateurs environnementaux.
- **NOAA**: prévisions et historiques météorologiques.
- **Global Flood Awareness System (GloFAS)**: risque inondation.

### 3) Données géospatiales et accessibilité

- **OpenStreetMap (OSM)**: routes, bâtiments, points d'intérêt, réseau logistique.
- **HOT (Humanitarian OpenStreetMap Team)**: cartographie de crise et zones sous-cartographiées.
- **Google Open Buildings / Microsoft Building Footprints** (selon pays): empreintes bâties.
- **SRTM / Copernicus DEM**: topographie et contraintes d'accès.

### 4) Santé publique et nutrition

- **OMS/WHO (surveillance épidémiologique)**: tendances maladies, alertes sanitaires.
- **UNICEF Data**: indicateurs nutrition, eau, assainissement et santé infantile.
- **DHS / MICS**: enquêtes ménages sur santé et vulnérabilité.

### 5) Contexte socio-économique

- **WorldPop / Meta High Resolution Population Density**: densité de population fine.
- **Banque mondiale Open Data**: pauvreté, développement, infrastructures.
- **IPC (Integrated Food Security Phase Classification)**: sécurité alimentaire.
- **FAOSTAT**: production agricole et facteurs liés à l'insécurité alimentaire.

### 6) Opérations internes ONG / agences

- Données de stock (entrepôts, ruptures), flotte et trajets, capacité des équipes, distributions passées.
- Données de feedback communautaire (helpdesk, enquêtes post-distribution).
- Journaux d'incidents sécurité et contraintes d'accès.

> Bonnes pratiques: commencer avec 5 à 10 sources robustes, harmoniser les identifiants géographiques (adm0/adm1/adm2), et tracer la qualité/fraîcheur de chaque source avant entraînement.

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
