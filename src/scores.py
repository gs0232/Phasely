"""
scores.py

Berechnet, wie gut die ausgewählten Sporteinheiten zur aktuellen Zyklusphase passen.
Gibt numerische Scores und eine tabellarische Übersicht zurück.
"""

import numpy as np
import pandas as pd


def calculate_match_scores(selected_sessions, current_phase):
    """
    Berechnet die Übereinstimmung der ausgewählten Sporteinheiten mit der aktuellen Zyklusphase.

    Args:
        selected_sessions (list): Liste von ausgewählten SportSession-Objekten.
        current_phase (CyclePhase): Aktuelle Zyklusphase.

    Returns:
        tuple:
            - df_scores (pd.DataFrame): Übersichtstabelle aller Einheiten.
            - final_score (float): Gesamtscore (1.0 = perfekte Übereinstimmung).
            - final_strength (float): Kraftanteil der Auswahl (0.0–1.0).
            - final_cardio (float): Ausdaueranteil der Auswahl (0.0–1.0).
            - final_low_impact (float): Low-Impact-Anteil der Auswahl (0.0–1.0).
            - avg_intensity (float): Durchschnittliche Trainingsintensität (0.0–1.0).
            - score_texts (dict): Prozentuale Werte als Strings für Anzeige.
    """
    if not selected_sessions:
        return (
            pd.DataFrame(), 0, 0, 0, 0, 0,
            {
                "overall": "–",
                "strength": "–",
                "cardio": "–",
                "low_impact": "–",
                "intensity": "–"
            },
        )

    def percent(x): return int(round(x * 100))

    # 1. Gesamtwerte pro Kategorie berechnen
    total_strength = sum(s.strength_score for s in selected_sessions)
    total_cardio = sum(s.cardio_score for s in selected_sessions)
    total_low_impact = sum(s.low_impact_score for s in selected_sessions)
    total = total_strength + total_cardio + total_low_impact

    if total == 0:
        return (
            pd.DataFrame(), 0, 0, 0, 0, 0,
            {
                "overall": "–",
                "strength": "–",
                "cardio": "–",
                "low_impact": "–",
                "intensity": "–"
            },
        )

    # 2. Normalisierte Verteilung der Anteile
    final_strength = total_strength / total
    final_cardio = total_cardio / total
    final_low_impact = total_low_impact / total

    # 3. Durchschnittliche Intensität berechnen
    avg_intensity = sum(s.intensity for s in selected_sessions) / len(selected_sessions)
    final_intensity_score = avg_intensity  # statt match-Wert

    # 4. Gesamtabweichung berechnen (je geringer, desto besser)
    deviation = (
        abs(current_phase.strength_score - final_strength) +
        abs(current_phase.cardio_score - final_cardio) +
        abs(current_phase.low_impact_score - final_low_impact)
    )
    final_score = 1.0 - deviation

    # 5. DataFrame mit Einzelwerten
    df_scores = pd.DataFrame([{
        "Ausgewählte Workouts": s.session_name,
        "Kraftanteil": f"{percent(s.strength_score)}%",
        "Ausdaueranteil": f"{percent(s.cardio_score)}%",
        "Low-Impact-Anteil": f"{percent(s.low_impact_score)}%",
        "Intensität": f"{percent(s.intensity)}%",
    } for s in selected_sessions])

    # 6. Score-Anzeige als Text
    score_percent_texts = {
        "overall": f"{percent(final_score)}%",
        "strength": f"{percent(final_strength)}%",
        "cardio": f"{percent(final_cardio)}%",
        "low_impact": f"{percent(final_low_impact)}%",
        "intensity": f"{percent(avg_intensity)}%"
    }

    return (
        df_scores,
        final_score,
        final_strength,
        final_cardio,
        final_low_impact,
        final_intensity_score,
        score_percent_texts,
    )
