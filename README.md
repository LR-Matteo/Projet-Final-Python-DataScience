# WindSpot 🌊⛵

> Trouvez le meilleur spot nautique selon les conditions météo du moment.

WindSpot croise la **base nationale RES** (Recensement des Équipements Sportifs) avec les données météo en temps réel (**Open-Meteo**) pour vous proposer les clubs, bases et installations nautiques avec les meilleures conditions pour votre sport.

**Sports supportés :** Voile · Planche à voile · Kitesurf

---

## Architecture

```
windspot/
├── app/
│   ├── main.py                  # Entrée FastAPI
│   ├── routers/
│   │   ├── search.py            # POST /api/search  (endpoint principal)
│   │   └── sports.py            # GET  /api/sports
│   ├── services/
│   │   ├── res_service.py       # Accès base RES (cache JSON + fallback API)
│   │   ├── weather_service.py   # Open-Meteo (vent, rafales, direction)
│   │   └── scoring_service.py   # Moteur de scoring par sport
│   └── models/
│       └── schemas.py           # Modèles Pydantic
├── frontend/
│   ├── templates/index.html     # Interface principale
│   └── static/
│       ├── css/style.css        # Design maritime
│       └── js/app.js            # Logique frontend (carte Leaflet, fetch)
├── data/
│   └── res_cache.json           # Cache local (généré par build_cache.py)
├── build_cache.py               # Script de construction du cache RES
└── requirements.txt
```

---

## Installation

```bash
# 1. Cloner le dépôt
git clone <repo>
cd windspot

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## Démarrage rapide

### Option A — Avec cache local (recommandé)

Construire le cache pour une zone géographique (ex : Bretagne et côtes atlantiques) :

```bash
# Zone autour de Nantes, rayon 300 km (couvre toute la façade atlantique)
python build_cache.py --lat 47.2 --lon -1.5 --radius 300

# Ou télécharger toute la France (plus long, ~5 min)
python build_cache.py --all-france
```

### Option B — Sans cache (fallback API automatique)

Lancez directement l'application, le cache sera alimenté à la première recherche.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Ouvrez **http://localhost:8000**

---

## Utilisation

1. **Choisissez votre sport** (Voile, Planche à voile, Kitesurf)
2. **Entrez vos coordonnées** ou cliquez sur "Ma position"
3. **Ajustez le rayon** de recherche (10–200 km)
4. **Définissez un score minimum** pour filtrer les conditions
5. Cliquez sur **Rechercher les spots**

Les résultats affichent :
- Les spots classés par **score de conditions** (0–100)
- Pour chaque spot : vent actuel, rafales, direction, température
- La **carte Leaflet** avec marqueurs colorés selon le score
- Le détail du scoring (vitesse vent, rafales, régularité)

---

## Scoring des conditions

Le score (0–100) est calculé en 3 composantes :

| Composante     | Poids | Critère                                         |
|----------------|-------|-------------------------------------------------|
| Vitesse vent   | 60 pts| Courbe trapézoïdale centrée sur la plage idéale |
| Rafales        | 25 pts| Pénalité progressive au-delà de 80% du max      |
| Régularité     | 15 pts| Ratio rafales/vent moyen                        |

### Profils par sport

| Sport           | Vent idéal   | Vent max | Rafales max |
|-----------------|-------------|----------|-------------|
| Voile           | 10–25 km/h  | 40 km/h  | 50 km/h     |
| Planche à voile | 18–35 km/h  | 55 km/h  | 65 km/h     |
| Kitesurf        | 20–40 km/h  | 60 km/h  | 70 km/h     |

### Étiquettes

| Score  | Label       |
|--------|-------------|
| ≥ 80   | Excellent   |
| 60–79  | Très bon    |
| 40–59  | Correct     |
| 20–39  | Médiocre    |
| < 20   | Impraticable|

---

## API REST

### `POST /api/search`

```json
{
  "latitude": 47.2184,
  "longitude": -1.5536,
  "radius_km": 50,
  "sport": "kitesurf"
}
```

Réponse : liste de spots avec score et conditions météo.

### `GET /api/sports`

Liste des sports disponibles avec profils de vent.

### `GET /health`

Vérification de l'état du service.

Documentation interactive : **http://localhost:8000/docs**

---

## Sources de données

- **Base RES** : [equipements.sports.gouv.fr](https://equipements.sports.gouv.fr) — Ministère des Sports (Open Data)
- **Météo** : [Open-Meteo](https://open-meteo.com) — API gratuite, sans clé, données ERA5 + GFS

---

## Évolutions possibles

- Prévisions météo sur 7 jours (Open-Meteo fournit des forecasts)
- Filtrage par direction de vent (offshore/onshore selon la côte)
- Historique des sessions et favoris (base SQLite)
- Alertes par email/push quand les conditions deviennent idéales
- Intégration des marées (API SHOM)
- Support d'autres sports (SUP, surf, canoë-kayak)
