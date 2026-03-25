'use strict';

// ─── État de l'application ───────────────────────────────────────────────────
let selectedSport = 'voile';
let map = null;
let markersLayer = null;
let currentResults = [];

const sportProfiles = {};  // Chargé depuis l'API au démarrage

// ─── Initialisation ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  initMap();
  initSportButtons();
  await loadSportProfiles();
  renderWindProfile('voile');
});

function initMap() {
  map = L.map('map', { zoomControl: true, attributionControl: true });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18,
  }).addTo(map);
  map.setView([47.2, -1.5], 8);
  markersLayer = L.layerGroup().addTo(map);
}

function initSportButtons() {
  document.querySelectorAll('.sport-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.sport-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedSport = btn.dataset.sport;
      renderWindProfile(selectedSport);
    });
  });
}

async function loadSportProfiles() {
  try {
    const resp = await fetch('/api/sports');
    const data = await resp.json();
    data.forEach(s => { sportProfiles[s.id] = s; });
  } catch (e) {
    console.error('Erreur chargement profils sports :', e);
  }
}

// ─── Profil vent ─────────────────────────────────────────────────────────────
function renderWindProfile(sportId) {
  const profile = sportProfiles[sportId];
  if (!profile) return;

  document.getElementById('sport-name').textContent = profile.label;

  const maxVal = profile.wind_range.max_gusts + 10;
  const rows = [
    { label: 'Vent min.', val: profile.wind_range.min, color: '#5ba4cf' },
    { label: 'Idéal bas', val: profile.wind_range.ideal_min, color: '#00b4d8' },
    { label: 'Idéal haut', val: profile.wind_range.ideal_max, color: '#0a3d62' },
    { label: 'Max vent', val: profile.wind_range.max, color: '#e07b39' },
    { label: 'Max rafales', val: profile.wind_range.max_gusts, color: '#cc2b2b' },
  ];

  document.getElementById('wind-bars').innerHTML = rows.map(r => `
    <div class="wind-bar-row">
      <span class="wind-bar-label">${r.label}</span>
      <div class="wind-bar-track">
        <div class="wind-bar-fill" style="width:${(r.val/maxVal*100).toFixed(1)}%;background:${r.color}"></div>
      </div>
      <span class="wind-bar-val">${r.val} km/h</span>
    </div>
  `).join('');
}

// ─── Géolocalisation ─────────────────────────────────────────────────────────
function geolocate() {
  if (!navigator.geolocation) {
    alert('Géolocalisation non disponible sur ce navigateur.');
    return;
  }
  navigator.geolocation.getCurrentPosition(
    pos => {
      document.getElementById('lat-input').value = pos.coords.latitude.toFixed(4);
      document.getElementById('lon-input').value = pos.coords.longitude.toFixed(4);
      map.setView([pos.coords.latitude, pos.coords.longitude], 10);
    },
    err => alert('Impossible de récupérer votre position : ' + err.message)
  );
}

// ─── Recherche ───────────────────────────────────────────────────────────────
async function doSearch() {
  const lat = parseFloat(document.getElementById('lat-input').value);
  const lon = parseFloat(document.getElementById('lon-input').value);
  const radius = parseInt(document.getElementById('radius-input').value);
  const minScore = parseInt(document.getElementById('score-threshold').value);

  if (isNaN(lat) || isNaN(lon)) {
    alert('Veuillez entrer des coordonnées valides.');
    return;
  }

  setLoading(true);

  try {
    const resp = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        latitude: lat,
        longitude: lon,
        radius_km: radius,
        sport: selectedSport,
      }),
    });

    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.detail || 'Erreur serveur');
    }

    const data = await resp.json();
    currentResults = data.results.filter(r => r.score >= minScore);
    renderResults(data, currentResults, minScore);
    updateMap(data, currentResults, lat, lon);

  } catch (e) {
    console.error(e);
    showError(e.message);
  } finally {
    setLoading(false);
  }
}

// ─── Rendu des résultats ─────────────────────────────────────────────────────
function renderResults(data, results, minScore) {
  const statsBar = document.getElementById('stats-bar');
  const list = document.getElementById('results-list');
  const empty = document.getElementById('empty-state');
  const mapOverlay = document.getElementById('map-overlay');

  mapOverlay.style.display = 'none';
  statsBar.style.display = 'flex';

  document.getElementById('stat-total').textContent = results.length;
  document.getElementById('stat-ideal').textContent = data.ideal_count;
  document.getElementById('stat-best').textContent =
    results.length > 0 ? `${results[0].score}/100` : '—';

  if (results.length === 0) {
    list.innerHTML = '';
    empty.style.display = 'flex';
    empty.querySelector('p').innerHTML =
      `Aucun spot avec un score ≥ ${minScore} dans cette zone.<br>
       Essayez un rayon plus grand ou un seuil plus bas.`;
    return;
  }

  empty.style.display = 'none';
  list.innerHTML = results.map((spot, i) => renderSpotCard(spot, i + 1)).join('');
}

function renderSpotCard(spot, rank) {
  const scoreClass = getScoreClass(spot.score);
  const rankClass = rank <= 3 ? `rank-${rank}` : '';

  const detailBars = [
    { name: 'Vitesse vent', s: spot.score_details.wind_speed, max: 60 },
    { name: 'Rafales', s: spot.score_details.gusts, max: 25 },
    { name: 'Régularité', s: spot.score_details.regularity, max: 15 },
  ];

  return `
  <div class="spot-card" onclick="focusSpot(${spot.latitude}, ${spot.longitude}, '${escapeHtml(spot.name)}')">
    <div>
      <div class="spot-header">
        <div class="spot-rank ${rankClass}">${rank}</div>
        <div>
          <div class="spot-name">${escapeHtml(spot.name)}
            <span class="distance-badge">📍 ${spot.distance_km} km</span>
          </div>
          <div class="spot-meta">${escapeHtml(spot.type_installation)} · ${escapeHtml(spot.city)}, ${escapeHtml(spot.department)}</div>
        </div>
      </div>
      <div class="spot-weather">
        <div class="weather-item">
          <span class="weather-icon">💨</span>
          <span class="weather-val">${spot.weather.wind_speed_kmh}</span>
          <span class="weather-lbl">km/h vent</span>
        </div>
        <div class="weather-item">
          <span class="weather-icon">🌬</span>
          <span class="weather-val">${spot.weather.wind_gusts_kmh}</span>
          <span class="weather-lbl">km/h rafales</span>
        </div>
        <div class="weather-item">
          <span class="weather-icon">🧭</span>
          <span class="weather-val">${spot.weather.wind_direction_label}</span>
          <span class="weather-lbl">${spot.weather.wind_direction_deg}°</span>
        </div>
        <div class="weather-item">
          <span class="weather-icon">🌡</span>
          <span class="weather-val">${spot.weather.temperature_c}°</span>
          <span class="weather-lbl">Celsius</span>
        </div>
      </div>
      <div class="score-details">
        ${detailBars.map(d => `
          <div class="score-bar-row">
            <span class="score-bar-name">${d.name}</span>
            <div class="score-bar-track">
              <div class="score-bar-inner" style="width:${(d.s.score/d.max*100).toFixed(1)}%"></div>
            </div>
            <span class="score-bar-comment">${d.s.label}</span>
          </div>
        `).join('')}
      </div>
    </div>
    <div class="score-badge score-${scoreClass}">
      <span class="score-num">${Math.round(spot.score)}</span>
      <span class="score-lbl-text">${spot.score_label}</span>
    </div>
  </div>`;
}

function getScoreClass(score) {
  if (score >= 80) return 'excellent';
  if (score >= 60) return 'good';
  if (score >= 40) return 'ok';
  return 'bad';
}

// ─── Carte ───────────────────────────────────────────────────────────────────
function updateMap(data, results, centerLat, centerLon) {
  markersLayer.clearLayers();

  // Marqueur du centre de recherche
  const centerIcon = L.divIcon({
    html: `<div style="width:14px;height:14px;background:#0a3d62;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 6px rgba(0,0,0,0.3)"></div>`,
    className: '',
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });
  L.marker([centerLat, centerLon], { icon: centerIcon })
    .addTo(markersLayer)
    .bindPopup('<b>Centre de recherche</b>');

  // Marqueurs des spots
  results.forEach((spot, i) => {
    const scoreClass = getScoreClass(spot.score);
    const color = { excellent: '#0d6e3a', good: '#1565a0', ok: '#7b5e00', bad: '#8b2020' }[scoreClass];

    const icon = L.divIcon({
      html: `<div style="
        width:32px;height:32px;
        background:${color};
        border-radius:50% 50% 50% 0;
        transform:rotate(-45deg);
        border:2px solid #fff;
        box-shadow:0 2px 8px rgba(0,0,0,0.3);
        display:flex;align-items:center;justify-content:center;
      ">
        <span style="transform:rotate(45deg);color:#fff;font-size:11px;font-weight:700;">${Math.round(spot.score)}</span>
      </div>`,
      className: '',
      iconSize: [32, 32],
      iconAnchor: [16, 32],
    });

    L.marker([spot.latitude, spot.longitude], { icon })
      .addTo(markersLayer)
      .bindPopup(`
        <b>${spot.name}</b><br>
        ${spot.type_installation}<br>
        💨 ${spot.weather.wind_speed_kmh} km/h · ${spot.weather.wind_direction_label}<br>
        Score : <b>${Math.round(spot.score)}/100</b> — ${spot.score_label}
      `);
  });

  // Ajuster le zoom sur les résultats
  if (results.length > 0) {
    const bounds = L.latLngBounds(
      results.map(s => [s.latitude, s.longitude]).concat([[centerLat, centerLon]])
    );
    map.fitBounds(bounds, { padding: [30, 30] });
  } else {
    map.setView([centerLat, centerLon], 10);
  }
}

function focusSpot(lat, lon, name) {
  map.setView([lat, lon], 13);
  markersLayer.eachLayer(layer => {
    if (layer.getLatLng && layer.getLatLng().lat === lat && layer.getLatLng().lng === lon) {
      layer.openPopup();
    }
  });
}

// ─── UI helpers ─────────────────────────────────────────────────────────────
function setLoading(on) {
  const btn = document.getElementById('search-btn');
  const loading = document.getElementById('loading');
  const list = document.getElementById('results-list');
  const empty = document.getElementById('empty-state');

  btn.disabled = on;
  loading.style.display = on ? 'flex' : 'none';
  if (on) { list.innerHTML = ''; empty.style.display = 'none'; }
}

function showError(msg) {
  const empty = document.getElementById('empty-state');
  empty.style.display = 'flex';
  empty.querySelector('p').innerHTML = `❌ Erreur : ${escapeHtml(msg)}`;
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
