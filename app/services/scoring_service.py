"""
Moteur de scoring des conditions météo par sport nautique.
Chaque sport a des plages de vent idéales, des rafales max et des critères propres.
Score final : 0–100.
"""
from dataclasses import dataclass


@dataclass
class SportProfile:
    label: str
    emoji: str
    min_wind_kmh: float      # Vent minimum utilisable
    ideal_min_kmh: float     # Vent idéal bas
    ideal_max_kmh: float     # Vent idéal haut
    max_wind_kmh: float      # Vent maximum praticable
    max_gusts_kmh: float     # Rafales dangereuses
    description: str


SPORT_PROFILES: dict[str, SportProfile] = {
    "voile": SportProfile(
        label="Voile",
        emoji="⛵",
        min_wind_kmh=5.0,
        ideal_min_kmh=10.0,
        ideal_max_kmh=25.0,
        max_wind_kmh=40.0,
        max_gusts_kmh=50.0,
        description="Vent régulier 10–25 km/h, rafales < 50 km/h",
    ),
    "planche_a_voile": SportProfile(
        label="Planche à voile",
        emoji="🏄",
        min_wind_kmh=12.0,
        ideal_min_kmh=18.0,
        ideal_max_kmh=35.0,
        max_wind_kmh=55.0,
        max_gusts_kmh=65.0,
        description="Vent soutenu 18–35 km/h, rafales < 65 km/h",
    ),
    "kitesurf": SportProfile(
        label="Kitesurf",
        emoji="🪁",
        min_wind_kmh=15.0,
        ideal_min_kmh=20.0,
        ideal_max_kmh=40.0,
        max_wind_kmh=60.0,
        max_gusts_kmh=70.0,
        description="Vent régulier 20–40 km/h, rafales < 70 km/h",
    ),
}


def score_wind_speed(speed: float, profile: SportProfile) -> tuple[float, str]:
    """
    Score 0–60 basé sur la vitesse du vent.
    La courbe est trapézoïdale : montée progressive → zone idéale (60 pts) → descente.
    """
    if speed < profile.min_wind_kmh:
        # Trop calme : score proportionnel à l'approche du minimum
        ratio = speed / profile.min_wind_kmh
        return round(ratio * 20, 1), "vent insuffisant"

    if profile.min_wind_kmh <= speed < profile.ideal_min_kmh:
        # Zone de transition basse
        ratio = (speed - profile.min_wind_kmh) / (profile.ideal_min_kmh - profile.min_wind_kmh)
        return round(20 + ratio * 40, 1), "vent léger"

    if profile.ideal_min_kmh <= speed <= profile.ideal_max_kmh:
        # Zone idéale : score maximal
        return 60.0, "vent idéal"

    if profile.ideal_max_kmh < speed <= profile.max_wind_kmh:
        # Zone de transition haute
        ratio = (speed - profile.ideal_max_kmh) / (profile.max_wind_kmh - profile.ideal_max_kmh)
        return round(60 - ratio * 40, 1), "vent fort"

    # Au-delà du maximum
    return 0.0, "vent trop fort"


def score_gusts(gusts: float, profile: SportProfile) -> tuple[float, str]:
    """Score 0–25 basé sur les rafales. Pénalité progressive au-delà de 80% du max."""
    safe_threshold = profile.max_gusts_kmh * 0.8

    if gusts <= safe_threshold:
        return 25.0, "rafales acceptables"

    if gusts <= profile.max_gusts_kmh:
        ratio = (gusts - safe_threshold) / (profile.max_gusts_kmh - safe_threshold)
        return round(25 - ratio * 20, 1), "rafales élevées"

    # Rafales dangereuses
    return 0.0, "rafales dangereuses"


def score_regularity(speed: float, gusts: float) -> tuple[float, str]:
    """
    Score 0–15 basé sur la régularité du vent (ratio rafales/vitesse).
    Un vent régulier (peu de turbulences) améliore la pratique.
    """
    if speed < 1.0:
        return 0.0, "pas de vent"

    ratio = gusts / speed
    if ratio <= 1.3:
        return 15.0, "vent très régulier"
    if ratio <= 1.6:
        return round(15 - (ratio - 1.3) / 0.3 * 10, 1), "vent assez régulier"
    if ratio <= 2.0:
        return round(5 - (ratio - 1.6) / 0.4 * 5, 1), "vent irrégulier"

    return 0.0, "vent très irrégulier"


def get_score_label(score: float) -> str:
    """Traduit le score numérique en label lisible."""
    if score >= 80:
        return "Excellent"
    if score >= 60:
        return "Très bon"
    if score >= 40:
        return "Correct"
    if score >= 20:
        return "Médiocre"
    return "Impraticable"


def compute_score(weather: dict, sport: str) -> dict:
    """
    Point d'entrée : calcule le score global et le détail pour un spot.

    Retourne:
      score       : float 0–100
      score_label : str
      details     : dict avec sous-scores et commentaires
    """
    profile = SPORT_PROFILES.get(sport)
    if not profile:
        raise ValueError(f"Sport inconnu : {sport}")

    wind_speed = weather.get("wind_speed_kmh", 0.0)
    wind_gusts = weather.get("wind_gusts_kmh", 0.0)

    s_speed, lbl_speed = score_wind_speed(wind_speed, profile)
    s_gusts, lbl_gusts = score_gusts(wind_gusts, profile)
    s_reg, lbl_reg = score_regularity(wind_speed, wind_gusts)

    total = round(s_speed + s_gusts + s_reg, 1)
    total = min(max(total, 0.0), 100.0)

    return {
        "score": total,
        "score_label": get_score_label(total),
        "score_details": {
            "wind_speed": {"score": s_speed, "max": 60, "label": lbl_speed},
            "gusts": {"score": s_gusts, "max": 25, "label": lbl_gusts},
            "regularity": {"score": s_reg, "max": 15, "label": lbl_reg},
        },
    }


def get_sport_profile(sport: str) -> SportProfile:
    profile = SPORT_PROFILES.get(sport)
    if not profile:
        raise ValueError(f"Sport inconnu : {sport}")
    return profile
