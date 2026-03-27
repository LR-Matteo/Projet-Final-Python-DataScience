"""
Router principal : endpoint POST /api/search
Orchestre RES + météo + scoring.
"""
import asyncio
import logging
from fastapi import APIRouter, HTTPException

from app.models.schemas import SearchRequest, SearchResponse, SpotResult, WeatherConditions
from app.services.res_service import get_spots_near
from app.services.weather_service import get_weather_batch
from app.services.scoring_service import compute_score, get_sport_profile, SPORT_PROFILES

logger = logging.getLogger(__name__)

router = APIRouter(tags=["search"])

MAX_SPOTS_PER_REQUEST = 30  # Limite pour éviter trop d'appels météo


@router.post("/search", response_model=SearchResponse)
async def search_spots(request: SearchRequest):
    """
    Recherche les spots nautiques autour des coordonnées données,
    récupère la météo pour chacun et retourne un score de conditions.
    """
    sport = request.sport.value
    profile = get_sport_profile(sport)

    # 1. Récupération des spots depuis la base RES
    logger.info(f"Recherche spots {sport} autour de ({request.latitude}, {request.longitude})")
    raw_spots = await get_spots_near(
        lat=request.latitude,
        lon=request.longitude,
        radius_km=request.radius_km,
        sport=sport,
    )

    if not raw_spots:
        return SearchResponse(
            sport=sport,
            sport_label=profile.label,
            sport_conditions={
                "min_wind_kmh": profile.min_wind_kmh,
                "max_wind_kmh": profile.max_wind_kmh,
                "ideal_wind_kmh": (profile.ideal_min_kmh + profile.ideal_max_kmh) / 2,
                "max_gusts_kmh": profile.max_gusts_kmh,
                "description": profile.description,
            },
            total_found=0,
            ideal_count=0,
            results=[],
            search_center={"latitude": request.latitude, "longitude": request.longitude},
        )

    # 2. Limitation pour ne pas surcharger l'API météo
    spots_to_process = raw_spots[:MAX_SPOTS_PER_REQUEST]

    # 3. Appels météo en parallèle
    coordinates = [(s["latitude"], s["longitude"]) for s in spots_to_process]
    weather_list = await get_weather_batch(coordinates)

    # 4. Scoring et construction des résultats
    results: list[SpotResult] = []
    for spot, weather in zip(spots_to_process, weather_list):
        if weather is None:
            logger.warning(f"Météo indisponible pour {spot['name']}, spot ignoré")
            continue

        scoring = compute_score(weather, sport)

        results.append(SpotResult(
            id=spot["id"],
            name=spot["name"],
            type_installation=spot["type_installation"],
            address=spot.get("address", ""),
            city=spot.get("city", ""),
            department=spot.get("department", ""),
            latitude=spot["latitude"],
            longitude=spot["longitude"],
            distance_km=spot["distance_km"],
            weather=WeatherConditions(**weather),
            score=scoring["score"],
            score_label=scoring["score_label"],
            score_details=scoring["score_details"],
        ))

    # 5. Tri par score décroissant
    results.sort(key=lambda r: r.score, reverse=True)

    ideal_count = sum(1 for r in results if r.score >= 60)

    return SearchResponse(
        sport=sport,
        sport_label=profile.label,
        sport_conditions={
            "min_wind_kmh": profile.min_wind_kmh,
            "max_wind_kmh": profile.max_wind_kmh,
            "ideal_wind_kmh": (profile.ideal_min_kmh + profile.ideal_max_kmh) / 2,
            "max_gusts_kmh": profile.max_gusts_kmh,
            "description": profile.description,
        },
        total_found=len(results),
        ideal_count=ideal_count,
        results=results,
        search_center={"latitude": request.latitude, "longitude": request.longitude},
    )
