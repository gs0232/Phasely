import streamlit as st
from src.data_setup import load_data, set_sport_sessions, set_cycle_phases
from src.classes import User


def get_main_data():
    """
    Gibt die geladenen Zyklusdaten zurück.
    """
    return st.session_state.get("main_data", None)


def get_user():
    """
    Gibt das User-Objekt aus dem Session-State zurück.
    """
    return st.session_state.get("current_user", None)


def get_sport_sessions():
    """
    Lädt die Sporteinheiten (falls nicht bereits vorhanden) und speichert sie im Session-State.
    """
    if "sport_sessions" not in st.session_state:
        sessions = set_sport_sessions("data/sport_sessions.csv")
        st.session_state.sport_sessions = sessions
    return st.session_state.sport_sessions


def get_cycle_phases():
    """
    Lädt die Zyklusphasen (falls nicht bereits vorhanden) und speichert sie im Session-State.
    """
    if "cycle_phases" not in st.session_state:
        phases = set_cycle_phases()
        st.session_state.cycle_phases = phases
    return st.session_state.cycle_phases


def get_current_index():
    """
    Gibt den Index des letzten historischen Tages zurück.
    """
    data = get_main_data()
    if data is not None:
        future_index = data[data["is_historic"] == False].index[0]
        return future_index - 1
    return None


def get_current_phase():
    """
    Gibt das aktuelle CyclePhase-Objekt zurück.
    """
    data = get_main_data()
    phases = get_cycle_phases()
    index = get_current_index()

    if data is None or index is None or phases is None:
        return None

    phase_name = data["phase"].iloc[index]
    for p in phases:
        if p.phase_name == phase_name:
            return p
    return None


def get_current_cycle_day():
    """
    Gibt den aktuellen Zyklustag zurück.
    """
    data = get_main_data()
    index = get_current_index()
    if data is not None and index is not None:
        return int(data["cycle_day"].iloc[index])
    return None


def get_next_phase():
    """
    Gibt die nächste Phase zurück (falls vorhanden).
    """
    current = get_current_phase()
    phases = get_cycle_phases()
    if current and phases:
        idx = phases.index(current)
        return phases[idx + 1] if idx + 1 < len(phases) else None
    return None


def get_color_palette():
    """
    Gibt das Farbschema zurück.
    """
    return {
        "Primary": "#CB997E",
        "Primary-light": "#DDBEA9",
        "Secondary": "#6B705C",
        "Secondary-light": "#A7AC9A",
        "Highlight": "#6665DD",
        "Highlight-light": "#9B9ECE"
    }
