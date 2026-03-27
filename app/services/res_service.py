import json, math, httpx, logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
CACHE_FILE = DATA_DIR / "res_cache.json"

RES_API_BASE = "https://equipements.sports.gouv.fr/api/explore/v2.1/catalog/datasets/data-es/records"

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlam = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def load_cache():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Cache charge : {len(data)} equipements")
            return data
        except Exception as e:
            logger.warning(f"Erreur cache : {e}")
    return []

def save_cache(data):
    DATA_DIR.mkdir(exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Cache sauvegarde : {len(data)} equipements")

async def _paginate(url, params, client):
    results, offset, limit = [], 0, params.get("limit", 100)
    while True:
        p = {**params, "offset": offset}
        try:
            resp = await client.get(url, params=p)
            if resp.status_code in (400, 404):
                logger.error(f"HTTP {resp.status_code} : {resp.text[:300]}")
                break
            resp.raise_for_status()
            batch = resp.json().get("results", [])
            if not batch:
                break
            results.extend(batch)
            offset += limit
            if len(batch) < limit:
                break
        except httpx.HTTPError as e:
            logger.error(f"Erreur reseau : {e}")
            break
    return results

async def fetch_from_api(lat, lon, radius_km):
    lat_delta = radius_km / 111.0
    lon_delta = radius_km / (111.0 * math.cos(math.radians(lat)))

    # Filtre geographique via geo_point_2d avec la syntaxe distance() de l'API
    # Alternative : bbox sur equip_coordonnees
    geo_where = (
        f"equip_coordonnees is not null "
        f"AND equip_coordonnees >= geom'POINT({lon-lon_delta:.4f} {lat-lat_delta:.4f})' "
    )
    # On utilise la fonction distance de l'API Opendatasoft
    geo_where = f"distance(equip_coordonnees, geom'POINT({lon:.6f} {lat:.6f})', {int(radius_km)}km)"

    params = {
        "where": geo_where,
        "limit": 100,
        "select": (
            "equip_numero,inst_numero,inst_nom,equip_nom,equip_type_name,"
            "inst_adresse,inst_cp,new_name,dep_nom,equip_coordonnees,aps_name"
        ),
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        logger.info(f"Appel API data-es : distance {radius_km}km autour de ({lat},{lon})")
        results = await _paginate(RES_API_BASE, params, client)

    logger.info(f"{len(results)} equipements recuperes")
    return results

def normalize_record(raw):
    lat = lon = None
    geo = raw.get("equip_coordonnees")
    if isinstance(geo, dict):
        lat = geo.get("lat")
        lon = geo.get("lon")
    try:
        lat = float(lat) if lat is not None else None
        lon = float(lon) if lon is not None else None
    except (ValueError, TypeError):
        lat = lon = None

    aps = raw.get("aps_name", "")
    if isinstance(aps, list):
        aps = " ".join(aps)

    return {
        "id": str(raw.get("equip_numero", raw.get("inst_numero", ""))),
        "name": raw.get("inst_nom") or raw.get("equip_nom") or "Equipement inconnu",
        "type_installation": raw.get("equip_type_name", "Non precise"),
        "address": raw.get("inst_adresse", ""),
        "postal_code": str(raw.get("inst_cp", "")),
        "city": raw.get("new_name", ""),
        "department": raw.get("dep_nom", ""),
        "latitude": lat,
        "longitude": lon,
        "activites": aps,
    }

def is_nautical(record):
    text = " ".join([
        record.get("type_installation", ""),
        record.get("name", ""),
        str(record.get("activites", "")),
    ]).lower()
    keywords = [
        "nautique", "voile", "planche", "kite", "port de plaisance",
        "plan d'eau", "plan d eau", "base nautique", "centre nautique",
        "windsurf", "cerf-volant", "club nautique", "ecole de voile",
        "surf", "marina", "aviron", "canoë", "canoe", "kayak",
    ]
    return any(kw in text for kw in keywords)

async def get_spots_near(lat, lon, radius_km, sport=None):
    cached = load_cache()
    if cached:
        raw_spots = cached
    else:
        raw_records = await fetch_from_api(lat, lon, radius_km * 2)
        raw_spots = [normalize_record(r) for r in raw_records]
        nautical = [s for s in raw_spots if is_nautical(s)]
        save_cache(nautical)
        raw_spots = nautical

    spots = []
    for spot in raw_spots:
        if not spot.get("latitude") or not spot.get("longitude"):
            continue
        dist = haversine_km(lat, lon, spot["latitude"], spot["longitude"])
        if dist <= radius_km:
            spot["distance_km"] = round(dist, 2)
            spots.append(spot)
    spots.sort(key=lambda s: s["distance_km"])
    logger.info(f"{len(spots)} spots dans {radius_km} km")
    return spots
