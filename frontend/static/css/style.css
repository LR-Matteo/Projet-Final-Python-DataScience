:root {
  --ocean: #0a3d62;
  --ocean-mid: #1e6fa8;
  --ocean-light: #5ba4cf;
  --sky: #e8f4fd;
  --wind: #00b4d8;
  --wind-light: #caf0f8;
  --foam: #f0f9ff;
  --sand: #fdf6ec;
  --text: #1a2332;
  --text-muted: #5a7a9a;
  --border: #d4e6f1;
  --excellent: #0d6e3a;
  --excellent-bg: #e6f7ef;
  --good: #1565a0;
  --good-bg: #e3f0fb;
  --ok: #7b5e00;
  --ok-bg: #fff8e1;
  --bad: #8b2020;
  --bad-bg: #fdecea;
  --radius: 12px;
  --radius-sm: 8px;
  --shadow: 0 2px 16px rgba(10,61,98,0.10);
  --shadow-hover: 0 6px 28px rgba(10,61,98,0.18);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--sky);
  color: var(--text);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ─── HEADER ─── */
.header {
  background: var(--ocean);
  padding: 18px 32px;
  display: flex;
  align-items: center;
  gap: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.2);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Syne', sans-serif;
  font-size: 24px;
  color: #fff;
  font-weight: 400;
}
.logo strong { font-weight: 800; color: var(--wind); }
.logo-icon { font-size: 26px; }

.header-tagline {
  color: rgba(255,255,255,0.6);
  font-size: 14px;
  font-weight: 300;
  letter-spacing: 0.02em;
  margin-left: auto;
}

/* ─── MAIN LAYOUT ─── */
.main {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 0;
  flex: 1;
  min-height: calc(100vh - 70px);
}

/* ─── SEARCH PANEL ─── */
.search-panel {
  background: #fff;
  border-right: 1px solid var(--border);
  padding: 24px 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.search-card, .wind-profile-card {
  background: var(--foam);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
}

.section-title {
  font-family: 'Syne', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--ocean);
  margin-bottom: 18px;
  letter-spacing: -0.01em;
}

.field-group { margin-bottom: 18px; }
.field-label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 8px;
}

/* Sport selector */
.sport-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
}
.sport-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 6px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  background: #fff;
  cursor: pointer;
  font-size: 11px;
  color: var(--text-muted);
  transition: all 0.15s;
  font-family: 'Inter', sans-serif;
}
.sport-btn:hover { border-color: var(--ocean-light); color: var(--ocean); }
.sport-btn.active {
  border-color: var(--wind);
  background: var(--wind-light);
  color: var(--ocean);
  font-weight: 500;
}
.sport-emoji { font-size: 20px; }

/* Geo inputs */
.input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px; }
.input-wrap { display: flex; flex-direction: column; gap: 4px; }
.input-label { font-size: 11px; color: var(--text-muted); }
.geo-input {
  width: 100%;
  padding: 8px 10px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 13px;
  color: var(--text);
  background: #fff;
  transition: border-color 0.15s;
  font-family: 'Inter', sans-serif;
}
.geo-input:focus { outline: none; border-color: var(--wind); }

.locate-btn {
  width: 100%;
  padding: 8px;
  background: transparent;
  border: 1.5px dashed var(--border);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
  font-family: 'Inter', sans-serif;
}
.locate-btn:hover { border-color: var(--wind); color: var(--ocean); background: var(--wind-light); }

/* Range inputs */
.range-input {
  width: 100%;
  height: 4px;
  -webkit-appearance: none;
  background: var(--border);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
  margin: 6px 0;
}
.range-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--wind);
  border: 2px solid #fff;
  box-shadow: 0 1px 6px rgba(0,180,216,0.4);
  cursor: pointer;
}
.range-labels {
  display: flex; justify-content: space-between;
  font-size: 10px; color: var(--text-muted);
}

/* Search button */
.search-btn {
  width: 100%;
  padding: 14px;
  background: var(--ocean);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s;
  letter-spacing: -0.01em;
}
.search-btn:hover { background: var(--ocean-mid); transform: translateY(-1px); }
.search-btn:active { transform: translateY(0); }
.search-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

/* Wind profile */
.wind-profile-card { padding: 16px; }
.wind-profile-title {
  font-family: 'Syne', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: var(--ocean);
  margin-bottom: 12px;
}

.wind-bars { display: flex; flex-direction: column; gap: 8px; }
.wind-bar-row { display: flex; align-items: center; gap: 8px; font-size: 11px; }
.wind-bar-label { width: 80px; color: var(--text-muted); text-align: right; flex-shrink: 0; }
.wind-bar-track {
  flex: 1;
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  position: relative;
  overflow: hidden;
}
.wind-bar-fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--ocean-light), var(--wind));
}
.wind-bar-val { width: 50px; color: var(--text); font-weight: 500; font-size: 11px; }

/* ─── RESULTS AREA ─── */
.results-area {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background: var(--sky);
}

/* Map */
.map-container {
  height: 320px;
  position: relative;
  flex-shrink: 0;
}
#map { height: 100%; width: 100%; }
.map-overlay {
  position: absolute; inset: 0;
  background: rgba(232,244,253,0.92);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  color: var(--text-muted);
  pointer-events: none;
  z-index: 999;
}

/* Stats bar */
.stats-bar {
  display: flex;
  gap: 0;
  background: var(--ocean);
  padding: 12px 24px;
  flex-shrink: 0;
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 20px;
  border-right: 1px solid rgba(255,255,255,0.15);
}
.stat-item:last-child { border-right: none; }
.stat-val {
  font-family: 'Syne', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  line-height: 1;
}
.stat-ideal .stat-val { color: var(--wind); }
.stat-lbl { font-size: 10px; color: rgba(255,255,255,0.55); margin-top: 3px; text-transform: uppercase; letter-spacing: 0.05em; }

/* Results list */
.results-list { padding: 20px 24px; display: flex; flex-direction: column; gap: 12px; }

/* Spot card */
.spot-card {
  background: #fff;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  padding: 16px 20px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  box-shadow: var(--shadow);
  transition: box-shadow 0.15s, transform 0.15s;
  cursor: pointer;
}
.spot-card:hover { box-shadow: var(--shadow-hover); transform: translateY(-2px); }

.spot-header { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 10px; }
.spot-rank {
  width: 28px; height: 28px;
  border-radius: 50%;
  background: var(--ocean);
  color: #fff;
  font-family: 'Syne', sans-serif;
  font-size: 12px;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.spot-rank.rank-1 { background: #c9a227; }
.spot-rank.rank-2 { background: #8e9aaf; }
.spot-rank.rank-3 { background: #a0522d; }

.spot-name {
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: var(--ocean);
  line-height: 1.2;
  margin-bottom: 3px;
}
.spot-meta { font-size: 12px; color: var(--text-muted); }

.spot-weather {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.weather-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 64px;
}
.weather-icon { font-size: 16px; margin-bottom: 2px; }
.weather-val {
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: var(--ocean-mid);
  line-height: 1;
}
.weather-lbl { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 1px; }

/* Score badge */
.score-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid currentColor;
  flex-shrink: 0;
  align-self: center;
}
.score-num {
  font-family: 'Syne', sans-serif;
  font-size: 24px;
  font-weight: 800;
  line-height: 1;
}
.score-lbl-text {
  font-size: 9px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  text-align: center;
  line-height: 1.2;
}

.score-excellent { color: var(--excellent); background: var(--excellent-bg); }
.score-good      { color: var(--good);      background: var(--good-bg); }
.score-ok        { color: var(--ok);        background: var(--ok-bg); }
.score-bad       { color: var(--bad);       background: var(--bad-bg); }

/* Score detail bar */
.score-details { margin-top: 10px; }
.score-bar-row { display: flex; align-items: center; gap: 8px; font-size: 11px; margin-bottom: 4px; }
.score-bar-name { width: 90px; color: var(--text-muted); }
.score-bar-track {
  flex: 1; height: 4px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
}
.score-bar-inner { height: 100%; border-radius: 2px; background: var(--wind); transition: width 0.4s; }
.score-bar-comment { font-size: 10px; color: var(--text-muted); width: 100px; }

/* Distance badge */
.distance-badge {
  display: inline-block;
  padding: 2px 8px;
  background: var(--sky);
  border: 1px solid var(--border);
  border-radius: 20px;
  font-size: 11px;
  color: var(--text-muted);
  margin-left: 8px;
}

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 60px 24px;
  color: var(--text-muted);
  font-size: 14px;
  line-height: 1.6;
  text-align: center;
}
.empty-icon { font-size: 48px; }

/* Loading */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 60px;
  color: var(--text-muted);
  font-size: 14px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.spinner {
  width: 36px; height: 36px;
  border: 3px solid var(--border);
  border-top-color: var(--wind);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* ─── RESPONSIVE ─── */
@media (max-width: 900px) {
  .main { grid-template-columns: 1fr; }
  .search-panel { border-right: none; border-bottom: 1px solid var(--border); }
  .map-container { height: 250px; }
  .header-tagline { display: none; }
}
