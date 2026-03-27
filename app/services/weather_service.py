"""
Service météo basé sur Open-Meteo (gratuit, sans clé API).
Récupère vent, rafales, direction et température pour des coordonnées GPS.
"""
import httpx
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

WIND_DIRECTIONS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"
]


def degrees_to_label(degrees: float) -> str:
    """Convertit des degrés de direction en label lisible (N, NE, SO, etc.)."""
    idx = round(degrees / 22.5) % 16
    return WIND_DIRECTIONS[idx]


async def get_weather(lat: float, lon: float) -> dict | None:
    """
    Récupère les conditions météo actuelles via Open-Meteo.
    Retourne vent (km/h), rafales, direction, température.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "windspeed_10m",
            "windgusts_10m",
            "winddirection_10m",
        ],
        "wind_speed_unit": "kmh",
        "timezone": "Europe/Paris",
        "forecast_days": 1,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(OPEN_METEO_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            current = data.get("current", {})

            wind_speed = current.get("windspeed_10m", 0.0)
            wind_gusts = current.get("windgusts_10m", 0.0)
            wind_dir = current.get("winddirection_10m", 0.0)
            temperature = current.get("temperature_2m", 15.0)

            return {
                "wind_speed_kmh": round(wind_speed, 1),
                "wind_gusts_kmh": round(wind_gusts, 1),
                "wind_direction_deg": round(wind_dir, 1),
                "wind_direction_label": degrees_to_label(wind_dir),
                "temperature_c": round(temperature, 1),
                "timestamp": current.get("time", datetime.now().isoformat()),
            }

        except httpx.TimeoutException:
            logger.warning(f"Timeout météo pour ({lat}, {lon})")
            return None
        except httpx.HTTPError as e:
            logger.error(f"Erreur API météo : {e}")
            return None


async def get_weather_batch(
    coordinates: list[tuple[float, float]],
    max_concurrent: int = 5,
) -> list[dict | None]:
    """
    Récupère la météo pour plusieurs coordonnées en parallèle (limitée).
    Open-Meteo supporte les requêtes groupées avec des listes de lat/lon.
    On regroupe par tranches pour respecter les limites.
    """
    import asyncio

    results = []
    for i in range(0, len(coordinates), max_concurrent):
        batch = coordinates[i:i + max_concurrent]
        tasks = [get_weather(lat, lon) for lat, lon in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=False)
        results.extend(batch_results)

    return results
