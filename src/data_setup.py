import pandas as pd
from src.classes import SportSession, CyclePhase


def load_data(file_path: str) -> pd.DataFrame:
    """
    Lädt CSV-Daten aus dem Zyklus-Tracking in ein DataFrame.
    
    Args:
        file_path (str): Pfad zur CSV-Datei.
    
    Returns:
        pd.DataFrame: Eingelesene Daten.
    """
    return pd.read_csv(file_path)


def set_sport_sessions(file_path: str):
    """
    Erstellt SportSession-Objekte aus CSV-Datei.
    
    Args:
        file_path (str): Pfad zur Datei mit den Sporteinheiten.
    
    Returns:
        tuple: Alle Sessions, Kraftsport-, Ausdauer- und Low-Impact-Sessions
    """
    data = load_data(file_path)
    sport_sessions = []

    for _, row in data.iterrows():
        session = SportSession(
            session_name=row["session_name"],
            category=row["category"],
            duration=row["duration"],
            intensity=row["intensity"],
            strength_score=row["strength_score"],
            cardio_score=row["cardio_score"],
            low_impact_score=row["low_impact_score"],
            is_selected=False
        )
        sport_sessions.append(session)

    strength = [s for s in sport_sessions if s.category == "Kraftsport"]
    cardio = [s for s in sport_sessions if s.category == "Ausdauersport"]
    low_impact = [s for s in sport_sessions if s.category == "Low Impact"]

    return sport_sessions, strength, cardio, low_impact


def set_cycle_phases():
    """
    Definiert die vier Zyklusphasen mit Werten.

    Returns:
        list: Liste von CyclePhase-Objekten.
    """
    def float_range(start, stop, step):
        values = []
        while start <= stop:
            values.append(round(start, 2))
            start += step
        return values

    return [
        CyclePhase("Menstruation", float_range(0.0, 0.2, 0.05), 0.2, 0.3, 0.5, 
            "Während der Periode eignet sich vor allem sanftes Training wie Yoga, Spazieren oder leichtes Radfahren. Die Intensitätskapazität ist niedrig, achte auf dein Wohlbefinden."),
        CyclePhase("Follikelphase", float_range(0.3, 0.5, 0.05), 0.55, 0.35, 0.10,
            "In dieser Phase bist du besonders leistungsfähig. Kraft- und Ausdauertraining dürfen fordernd sein, dein Körper regeneriert schnell."),
        CyclePhase("Ovulation", float_range(0.5, 0.8, 0.05), 0.50, 0.40, 0.10,
            "Rund um den Eisprung ist deine Koordination und Stärke auf einem Höhepunkt. Jetzt sind anspruchsvolle Workouts ideal – aber achte auf Verletzungsrisiken."),
        CyclePhase("Lutealphase", float_range(0.8, 1.0, 0.05), 0.30, 0.25, 0.45,
            "Die Leistung sinkt wieder, viele fühlen sich aufgebläht oder müde. Low-Impact-Training hilft dir, aktiv zu bleiben und PMS zu lindern.")
    ]
