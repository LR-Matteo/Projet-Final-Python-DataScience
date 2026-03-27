#!/usr/bin/env python3
"""
Script de construction du cache RES local.
Telecharge les equipements nautiques depuis data.gouv.fr et les sauvegarde en JSON.

Usage:
  python build_cache.py --all-france
  python build_cache.py --lat 47.2 --lon -1.5 --radius 300
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

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
    "radius_km": 1200,
}


async def build_cache_france():
    """Telecharge tous les equipements nautiques de France."""
    print("Telechargement des equipements nautiques depuis data.gouv.fr...")
    print("(Cela peut prendre quelques minutes)\n")

    raw = await fetch_from_api(
        lat=FULL_FRANCE_BBOX["lat"],
        lon=FULL_FRANCE_BBOX["lon"],
        radius_km=FULL_FRANCE_BBOX["radius_km"],
    )
    print(f"OK - {len(raw)} equipements recuperes depuis l'API")

    normalized = [normalize_record(r) for r in raw]
    nautical = [s for s in normalized if is_nautical(s)]
    print(f"OK - {len(nautical)} equipements nautiques filtres")

    valid = [s for s in nautical if s.get("latitude") and s.get("longitude")]
    print(f"OK - {len(valid)} equipements avec coordonnees GPS valides")

    save_cache(valid)
    print(f"\nCache sauvegarde dans {DATA_DIR / 'res_cache.json'}")
    print(f"{len(valid)} spots prets a l'utilisation.")


async def build_cache_zone(lat: float, lon: float, radius_km: float):
    """Telecharge les equipements nautiques dans une zone donnee."""
    print(f"Telechargement pour la zone ({lat}, {lon}) - rayon {radius_km} km...")

    raw = await fetch_from_api(lat=lat, lon=lon, radius_km=radius_km)
    print(f"OK - {len(raw)} equipements recuperes")

    normalized = [normalize_record(r) for r in raw]
    nautical = [s for s in normalized if is_nautical(s)]
    valid = [s for s in nautical if s.get("latitude") and s.get("longitude")]
    print(f"OK - {len(valid)} equipements nautiques avec coordonnees GPS")

    # Fusion avec le cache existant
    cache_path = DATA_DIR / "res_cache.json"
    existing = []
    if cache_path.exists():
        with open(cache_path) as f:
            existing = json.load(f)
        print(f"Cache existant : {len(existing)} entrees")

    existing_ids = {s["id"] for s in existing}
    new_entries = [s for s in valid if s["id"] not in existing_ids]
    merged = existing + new_entries
    print(f"{len(new_entries)} nouveaux equipements ajoutes")

    save_cache(merged)
    print(f"\nCache mis a jour : {len(merged)} spots au total")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Construction du cache RES local")
    parser.add_argument("--all-france", action="store_true",
                        help="Telecharge toute la France")
    parser.add_argument("--lat", type=float, help="Latitude du centre")
    parser.add_argument("--lon", type=float, help="Longitude du centre")
    parser.add_argument("--radius", type=float, default=200,
                        help="Rayon en km (defaut: 200)")
    args = parser.parse_args()

    if args.all_france:
        asyncio.run(build_cache_france())
    elif args.lat is not None and args.lon is not None:
        asyncio.run(build_cache_zone(args.lat, args.lon, args.radius))
    else:
        print("Usage:")
        print("  python build_cache.py --all-france")
        print("  python build_cache.py --lat 47.2 --lon -1.5 --radius 300")
        sys.exit(1)
