from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SportType(str, Enum):
    voile = "voile"
    planche_a_voile = "planche_a_voile"
    kitesurf = "kitesurf"


class SearchRequest(BaseModel):
    latitude: float = Field(..., description="Latitude du centre de recherche", ge=-90, le=90)
    longitude: float = Field(..., description="Longitude du centre de recherche", ge=-180, le=180)
    radius_km: float = Field(50.0, description="Rayon de recherche en km", ge=1, le=300)
    sport: SportType = Field(..., description="Sport nautique ciblé")


class WeatherConditions(BaseModel):
    wind_speed_kmh: float
    wind_gusts_kmh: float
    wind_direction_deg: float
    wind_direction_label: str
    temperature_c: float
    timestamp: str


class SportConditions(BaseModel):
    min_wind_kmh: float
    max_wind_kmh: float
    ideal_wind_kmh: float
    max_gusts_kmh: float
    description: str


class SpotResult(BaseModel):
    id: str
    name: str
    type_installation: str
    address: str
    city: str
    department: str
    latitude: float
    longitude: float
    distance_km: float
    weather: WeatherConditions
    score: float = Field(..., description="Score 0-100 des conditions météo", ge=0, le=100)
    score_label: str
    score_details: dict


class SearchResponse(BaseModel):
    sport: str
    sport_label: str
    sport_conditions: SportConditions
    total_found: int
    ideal_count: int
    results: list[SpotResult]
    search_center: dict
