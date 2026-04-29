# 🌊 WINDSPOT
 
> Trouvez le meilleur spot nautique autour de vous selon les conditions météo du moment.
 
---
 
## Présentation
 
**WINDSPOT** est un outil d'aide à la décision pour les pratiquants de sports nautiques. En renseignant une ville, un rayon de recherche et une discipline, l'application identifie l'équipement nautique le plus proche offrant les meilleures conditions météorologiques pour votre activité.
 
---
 
## Sources de données
 
| Source | Contenu |
|---|---|
| [data.gouv.fr](https://www.data.gouv.fr) | Recensement des équipements sportifs, espaces et sites de pratiques |
| [Open-Meteo](https://open-meteo.com) | Données météorologiques via API |
 
---
 
## Variables retenues
 
### Équipements sportifs
 
Les colonnes suivantes ont été conservées depuis la base brute :
 
| Colonne | Description |
|---|---|
| `equip_numero`, `inst_numero` | Identifiants uniques |
| `inst_nom`, `inst_adresse`, `inst_cp` | Informations de localisation |
| `dep_code`, `dep_nom` | Département |
| `reg_code`, `reg_nom` | Région |
| `lib_bdv` | Ville |
| `equip_nom`, `equip_type_name` | Nom et type d'équipement |
| `equip_coordonnees` | Coordonnées GPS |
| `aps_name` | Activités proposées |
 
### Météo
 
Seules les variables intervenant dans le calcul du score par sport ont été conservées.
 
---
 
## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/windspot.git
cd windspot
```

### 2. Installer les dépendances
 
```bash
pip install -r requirement.txt
```
 
---
 
## Lancement
 
Les notebooks doivent être exécutés **dans l'ordre suivant** :
 
1. `bdd_stats_desc.ipynb` — Statistiques descriptives et exploration de la base
2. `acp_clustering.ipynb` — ACP et clustering des équipements
3. `windspot.ipynb` — Application finale : recherche du meilleur spot
---
 
## Méthodologie
 
### 1. Statistiques descriptives
 
Exploration de la base des équipements sportifs via :
 
- Répartition des équipements par département et par région
- Analyse des types d'équipements présents
- Cartographies de visualisation
- Création d'une sous-base dédiée aux **équipements nautiques**
### 2. Modélisation : ACP + Clustering
 
Une Analyse en Composantes Principales (ACP) suivie d'un clustering a été appliquée sur l'ensemble des équipements afin de mettre en évidence des **différences spatiales** dans leur répartition sur le territoire. Les profils identifiés regroupent par exemple :
 
- Les équipements à dominante ultramarine
- Les équipements de sports de nature en extérieur
- Les équipements liés à de fortes densités de population
### 3. Score météo et recommandation
 
Un score adapté à chaque sport nautique a été construit à partir des variables météo. À partir d'une ville, d'un rayon et d'une discipline, l'application retourne **l'équipement le plus proche affichant les meilleures conditions météo** pour la pratique choisie.