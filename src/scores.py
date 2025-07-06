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
            pd.DataFrame(), 0, 0, 0, 0,
            None, None,
            {"overall": "–", "strength": "–", "cardio": "–", "low_impact": "–"}
        )

    # Initialisierung
    total_strength, total_cardio, total_low_impact, total_intensity = 0, 0, 0, 0

    # Match-Scores berechnen
    for session in selected_sessions:
        session.match_score = (
            1
            - abs(current_phase.strength_score - session.strength_score)
            - abs(current_phase.cardio_score - session.cardio_score)
            - abs(current_phase.low_impact_score - session.low_impact_score)
            - abs(current_phase.training_intensity - session.intensity)
        ) / 4  # Normiert auf 0–1

        total_strength += session.strength_score
        total_cardio += session.cardio_score
        total_low_impact += session.low_impact_score
        total_intensity += session.intensity

    # Durchschnittswerte berechnen
    n = len(selected_sessions)
    avg_strength = total_strength / n
    avg_cardio = total_cardio / n
    avg_low_impact = total_low_impact / n
    avg_intensity = total_intensity / n

    # Finaler Gesamtscore (je geringer die Abweichung, desto besser)
    final_score = (
        1
        - abs(current_phase.strength_score - avg_strength)
        - abs(current_phase.cardio_score - avg_cardio)
        - abs(current_phase.low_impact_score - avg_low_impact)
        - abs(current_phase.training_intensity - avg_intensity)
    ) / 4

    # Runde alles für Anzeige
    def percent(x):
        # Wenn x ein ndarray ist, nimm das erste Element
        if isinstance(x, (np.ndarray, list)):
            x = x[0]
        return int(round(x * 100))


    df = pd.DataFrame([
        {
            "Workout": s.session_name,
            "Match": f"{percent(s.match_score)}%"
        }
        for s in selected_sessions
    ])

    #best_session = max(selected_sessions, key=lambda s: float(s.match_score), default=None)
    #worst_session = min(selected_sessions, key=lambda s: float(s.match_score), default=None)

    score_percent_texts = {
        "overall": f"{percent(final_score)}%",
        "strength": f"{percent(1 - abs(current_phase.strength_score - avg_strength))}%",
        "cardio": f"{percent(1 - abs(current_phase.cardio_score - avg_cardio))}%",
        "low_impact": f"{percent(1 - abs(current_phase.low_impact_score - avg_low_impact))}%"
    }

    return (
        df,
        percent(final_score) / 100,
        percent(1 - abs(current_phase.strength_score - avg_strength)) / 100,
        percent(1 - abs(current_phase.cardio_score - avg_cardio)) / 100,
        percent(1 - abs(current_phase.low_impact_score - avg_low_impact)) / 100,
        #best_session.session_name if best_session else "–",
        #worst_session.session_name if worst_session else "–",
        score_percent_texts
    )
