#!/usr/bin/env python3
"""
Script de construction du cache RES local.
Télécharge les équipements nautiques depuis data.gouv.fr et les sauvegarde en JSON.
Usage : python build_cache.py [--all-france] [--lat LAT --lon LON --radius KM]

Sans argument → télécharge tous les équipements nautiques de France.
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

# Ajout du répertoire parent au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.res_service import (
    fetch_from_api,
    normalize_record,
    is_nautical,
    save_cache,
    DATA_DIR,
)

FULL_FRANCE_BBOX = {
    "lat": 46.5,
    "lon": 2.5,
    "radius_km": 1200,  # Couvre la France métropolitaine + côtes
}


async def build_cache_france():
    """Télécharge tous les équipements nautiques de France."""
    print("📡 Téléchargement des équipements nautiques depuis data.gouv.fr...")
    print("   (Cela peut prendre quelques minutes selon le réseau)\n")

    raw = await fetch_from_api(
        lat=FULL_FRANCE_BBOX["lat"],
        lon=FULL_FRANCE_BBOX["lon"],
        radius_km=FULL_FRANCE_BBOX["radius_km"],
    )
    print(f"✓ {len(raw)} équipements récupérés depuis l'API")

    normalized = [normalize_record(r) for r in raw]
    nautical = [s for s in normalized if is_nautical(s)]
    print(f"✓ {len(nautical)} équipements nautiques filtrés")

    valid = [s for s in nautical if s.get("latitude") and s.get("longitude")]
    print(f"✓ {len(valid)} équipements avec coordonnées GPS valides")

    save_cache(valid)
    print(f"\n✅ Cache sauvegardé dans {DATA_DIR / 'res_cache.json'}")
    print(f"   {len(valid)} spots prêts à l'utilisation.")


async def build_cache_zone(lat: float, lon: float, radius_km: float):
    """Télécharge les équipements nautiques dans une zone donnée."""
    print(f"📡 Téléchargement pour la zone ({lat}, {lon}) dans un rayon de {radius_km} km...")

    raw = await fetch_from_api(lat=lat, lon=lon, radius_km=radius_km)
    print(f"✓ {len(raw)} équipements récupérés")

    normalized = [normalize_record(r) for r in raw]
    nautical = [s for s in normalized if is_nautical(s)]
    valid = [s for s in nautical if s.get("latitude") and s.get("longitude")]

    print(f"✓ {len(valid)} équipements nautiques avec coordonnées GPS")

    # Merge avec le cache existant si présent
    cache_path = DATA_DIR / "res_cache.json"
    existing = []
    if cache_path.exists():
        with open(cache_path) as f:
            existing = json.load(f)
        print(f"✓ Cache existant : {len(existing)} entrées")

    existing_ids = {s["id"] for s in existing}
    new_entries = [s for s in valid if s["id"] not in existing_ids]
    merged = existing + new_entries
    print(f"✓ {len(new_entries)} nouveaux équipements ajoutés")

    save_cache(merged)
    print(f"\n✅ Cache mis à jour : {len(merged)} spots total")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Construction du cache RES local")
    parser.add_argument("--all-france", action="store_true", help="Télécharge toute la France")
    parser.add_argument("--lat", type=float, help="Latitude du centre")
    parser.add_argument("--lon", type=float, help="Longitude du centre")
    parser.add_argument("--radius", type=float, default=200, help="Rayon en km (défaut: 200)")
    args = parser.parse_args()

    if args.all_france:
        asyncio.run(build_cache_france())
    elif args.lat and args.lon:
        asyncio.run(build_cache_zone(args.lat, args.lon, args.radius))
    else:
        print("Usage :")
        print("  python build_cache.py --all-france")
        print("  python build_cache.py --lat 47.2 --lon -1.5 --radius 150")
