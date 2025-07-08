"""
scores.py

Berechnet, wie gut ausgewählte Sporteinheiten zur aktuellen Zyklusphase passen.
Gibt Einzelwerte, Gesamtwerte und Score-Texte zurück.
"""

import numpy as np
import pandas as pd


def calculate_match_scores(selected_sessions, current_phase):
    """
    Berechnet die Übereinstimmung ausgewählter Sporteinheiten mit der aktuellen Zyklusphase.

    Args:
        selected_sessions (list): Liste von SportSession-Objekten.
        current_phase (CyclePhase): Aktuelle Phase der Nutzerin.

    Returns:
        tuple: (
            pd.DataFrame: Übersicht der ausgewählten Einheiten,
            float: Finaler Gesamtscore (0.0–1.0),
            float: Finaler Kraft-Score,
            float: Finaler Ausdauer-Score,
            float: Finaler Low-Impact-Score,
            float: Durchschnittliche Intensität (0.0–1.0),
            dict: Score-Texte für Anzeige (Prozentangaben als Strings)
        )
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

    # 3. Durchschnittliche Intensität der Auswahl
    avg_intensity = sum(s.intensity for s in selected_sessions) / len(selected_sessions)
    final_intensity_score = avg_intensity

    # 4. Berechne finalen Gesamtscore (Abweichung von Phase-Werten)
    deviation = (
        abs(current_phase.strength_score - final_strength) +
        abs(current_phase.cardio_score - final_cardio) +
        abs(current_phase.low_impact_score - final_low_impact)
    )
    final_score = 1.0 - deviation

    # 5. DataFrame zur Anzeige
    df = pd.DataFrame([{
        "Ausgewählte Workouts": s.session_name,
        "Kraftanteil": f"{percent(s.strength_score)}%",
        "Ausdaueranteil": f"{percent(s.cardio_score)}%",
        "Low-Impact-Anteil": f"{percent(s.low_impact_score)}%",
        "Intensität": f"{percent(s.intensity)}%",
    } for s in selected_sessions])

    # 6. Score-Texte zur Anzeige
    score_percent_texts = {
        "overall": f"{percent(final_score)}%",
        "strength": f"{percent(final_strength)}%",
        "cardio": f"{percent(final_cardio)}%",
        "low_impact": f"{percent(final_low_impact)}%",
        "intensity": f"{percent(final_intensity_score)}%"
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
