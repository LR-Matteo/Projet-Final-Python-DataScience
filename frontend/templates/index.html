<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WindSpot — Trouvez votre spot idéal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

<header class="header">
  <div class="logo">
    <span class="logo-icon">⛵</span>
    <span class="logo-text">Wind<strong>Spot</strong></span>
  </div>
  <p class="header-tagline">Le meilleur spot selon le vent, maintenant.</p>
</header>

<main class="main">

  <!-- Panneau de recherche -->
  <aside class="search-panel">
    <div class="search-card">
      <h2 class="section-title">Votre recherche</h2>

      <!-- Sport -->
      <div class="field-group">
        <label class="field-label">Sport pratiqué</label>
        <div class="sport-grid" id="sport-selector">
          <button class="sport-btn active" data-sport="voile">
            <span class="sport-emoji">⛵</span>
            <span>Voile</span>
          </button>
          <button class="sport-btn" data-sport="planche_a_voile">
            <span class="sport-emoji">🏄</span>
            <span>Planche à voile</span>
          </button>
          <button class="sport-btn" data-sport="kitesurf">
            <span class="sport-emoji">🪁</span>
            <span>Kitesurf</span>
          </button>
        </div>
      </div>

      <!-- Zone géographique -->
      <div class="field-group">
        <label class="field-label">Zone de recherche</label>
        <div class="geo-inputs">
          <div class="input-row">
            <div class="input-wrap">
              <label class="input-label">Latitude</label>
              <input type="number" id="lat-input" class="geo-input" step="0.0001"
                     value="47.2184" placeholder="47.2184">
            </div>
            <div class="input-wrap">
              <label class="input-label">Longitude</label>
              <input type="number" id="lon-input" class="geo-input" step="0.0001"
                     value="-1.5536" placeholder="-1.5536">
            </div>
          </div>
          <button class="locate-btn" onclick="geolocate()">
            📍 Ma position
          </button>
        </div>
      </div>

      <!-- Rayon -->
      <div class="field-group">
        <label class="field-label">
          Rayon de recherche : <strong id="radius-val">50 km</strong>
        </label>
        <input type="range" id="radius-input" class="range-input"
               min="10" max="200" step="10" value="50"
               oninput="document.getElementById('radius-val').textContent = this.value + ' km'">
        <div class="range-labels">
          <span>10 km</span><span>200 km</span>
        </div>
      </div>

      <!-- Seuil de score -->
      <div class="field-group">
        <label class="field-label">
          Score minimum : <strong id="score-val">40</strong>/100
        </label>
        <input type="range" id="score-threshold" class="range-input"
               min="0" max="90" step="10" value="40"
               oninput="document.getElementById('score-val').textContent = this.value">
        <div class="range-labels">
          <span>Tous</span><span>Excellent seulement</span>
        </div>
      </div>

      <button class="search-btn" onclick="doSearch()" id="search-btn">
        <span class="btn-icon">🔍</span>
        Rechercher les spots
      </button>
    </div>

    <!-- Profil vent du sport -->
    <div class="wind-profile-card" id="wind-profile">
      <h3 class="wind-profile-title">Profil vent — <span id="sport-name">Voile</span></h3>
      <div class="wind-bars" id="wind-bars"></div>
    </div>
  </aside>

  <!-- Zone résultats -->
  <section class="results-area">

    <!-- Carte -->
    <div class="map-container">
      <div id="map"></div>
      <div class="map-overlay" id="map-overlay">
        <p>Lancez une recherche pour voir les spots sur la carte</p>
      </div>
    </div>

    <!-- Stats rapides -->
    <div class="stats-bar" id="stats-bar" style="display:none">
      <div class="stat-item">
        <span class="stat-val" id="stat-total">0</span>
        <span class="stat-lbl">spots trouvés</span>
      </div>
      <div class="stat-item stat-ideal">
        <span class="stat-val" id="stat-ideal">0</span>
        <span class="stat-lbl">conditions idéales</span>
      </div>
      <div class="stat-item">
        <span class="stat-val" id="stat-best">—</span>
        <span class="stat-lbl">meilleur score</span>
      </div>
    </div>

    <!-- Liste des spots -->
    <div id="results-list" class="results-list"></div>

    <!-- État vide -->
    <div class="empty-state" id="empty-state">
      <div class="empty-icon">🌊</div>
      <p>Sélectionnez votre sport et une zone géographique,<br>puis lancez la recherche.</p>
    </div>

    <!-- Loading -->
    <div class="loading" id="loading" style="display:none">
      <div class="spinner"></div>
      <p>Analyse des spots et conditions météo en cours…</p>
    </div>

  </section>
</main>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="/static/js/app.js"></script>
</body>
</html>
