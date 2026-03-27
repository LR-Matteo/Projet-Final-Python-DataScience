from fastapi import APIRouter
from app.services.scoring_service import SPORT_PROFILES

router = APIRouter(tags=["sports"])


@router.get("/sports")
async def list_sports():
    """Retourne la liste des sports disponibles avec leurs profils de vent."""
    return [
        {
            "id": sport_id,
            "label": p.label,
            "emoji": p.emoji,
            "description": p.description,
            "wind_range": {
                "min": p.min_wind_kmh,
                "ideal_min": p.ideal_min_kmh,
                "ideal_max": p.ideal_max_kmh,
                "max": p.max_wind_kmh,
                "max_gusts": p.max_gusts_kmh,
            },
        }
        for sport_id, p in SPORT_PROFILES.items()
    ]
