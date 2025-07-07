import numpy as np
import pandas as pd

def calculate_match_scores(selected_sessions, current_phase):
    """
    Berechnet, wie gut die ausgewählten Sporteinheiten zur aktuellen Zyklusphase passen.

    Rückgabe:
    - DataFrame mit Einzelwerten pro Einheit
    - Finaler Gesamtscore (Ø)
    - Finaler Kraft-, Ausdauer- und Low-Impact-Score (Ø)
    - Beste und schlechteste Einheit nach Match Score
    """
    if not selected_sessions:
        return (
            pd.DataFrame(), 0, 0, 0, 0, 0,
            {"overall": "–", "strength": "–", "cardio": "–", "low_impact": "–", "intensity": "–"},
        )

    def percent(x): return int(round(x * 100))

    # 1. Summiere die Anteile der Kategorien
    total_strength = sum(s.strength_score for s in selected_sessions)
    total_cardio = sum(s.cardio_score for s in selected_sessions)
    total_low_impact = sum(s.low_impact_score for s in selected_sessions)

    total = total_strength + total_cardio + total_low_impact
    if total == 0:
        return (
            pd.DataFrame(), 0, 0, 0, 0, 0,
            {"overall": "–", "strength": "–", "cardio": "–", "low_impact": "–", "intensity": "–"},
        )

    # 2. Prozentuelle Verteilung (normiert auf 100 %)
    final_strength = total_strength / total
    final_cardio = total_cardio / total
    final_low_impact = total_low_impact / total

    # 3. Berechne durchschnittliche Intensität (separat)
    avg_intensity = sum(s.intensity for s in selected_sessions) / len(selected_sessions)

    # 4. Intensitäts-Match (1.0 = perfekt, sonst linearer Abzug)
    def match_training_intensity(intensity):
        min_int = min(current_phase.training_intensity)
        max_int = max(current_phase.training_intensity)
        if min_int <= intensity <= max_int:
            return 1.0
        diff = abs(intensity - min_int) if intensity < min_int else abs(intensity - max_int)
        return max(0.0, 1.0 - diff)

    final_intensity_score = match_training_intensity(avg_intensity)

    # 5. Berechne finalen Gesamtscore (je geringer die Abweichung, desto besser)
    deviation = (
        abs(current_phase.strength_score - final_strength) +
        abs(current_phase.cardio_score - final_cardio) +
        abs(current_phase.low_impact_score - final_low_impact)
    )
    final_score = 1.0 - deviation  # max 1.0 → beste Übereinstimmung

    # 6. DataFrame zur Darstellung
    df = pd.DataFrame([{
        "Ausgewählte Workouts": s.session_name,
        "Kraftanteil": f"{percent(s.strength_score)}%",
        "Ausdaueranteil": f"{percent(s.cardio_score)}%",
        "Low-Impact-Anteil": f"{percent(s.low_impact_score)}%",
        "Intensität": f"{percent(s.intensity)}%",
    } for s in selected_sessions])

    # 7. Text-Scores für Anzeige
    score_percent_texts = {
        "overall": f"{percent(final_score)}%",
        "strength": f"{percent(final_strength)}%",
        "cardio": f"{percent(final_cardio)}%",
        "low_impact": f"{percent(final_low_impact)}%",
        "intensity": f"{percent(avg_intensity)}%" if final_intensity_score > 0 else "0%"
    }

    return (
        df,
        final_score,
        final_strength,
        final_cardio,
        final_low_impact,
        final_intensity_score,
        score_percent_texts,
    )
