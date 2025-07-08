"""
00_Dashboard.py

Einseitige App-Version von Phasely mit integriertem Startscreen.
Wechselt bei vollständiger Eingabe automatisch in das Dashboard.
"""

import streamlit as st
import pandas as pd

from src.classes import User
from src.data_setup import load_data, set_sport_sessions, set_cycle_phases
from src.globals import (
    get_color_palette, get_current_cycle_day, get_current_phase
)
from src.interface_components import (
    h1, h2, h3, textblock, view_score_percentage,
    info_card, button
)
from src.modules import (
    show_selection, show_match_scores, current_cycle_plot_2
)

#%% Initialisierung
st.set_page_config(
    page_title="Phasely",
    page_icon=":heart:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialisierungs-Flags
if "has_started" not in st.session_state:
    st.session_state.has_started = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

#%% Startscreen
if not st.session_state.has_started:

    h1("Willkommen bei Phasely")
    textblock("👋 Bevor es losgeht, sag uns kurz deinen Namen, dein Alter und lade deine Zyklusdaten hoch.")

    with st.form("user_form"):
        name = st.text_input("Vorname", placeholder="z. B. Heidi")
        age = st.number_input("Alter", min_value=10, max_value=100, value=25, step=1)
        uploaded_file = st.file_uploader("Zyklus-Tracking CSV-Datei", type=["csv"])
        submitted = st.form_submit_button("Daten hochladen")

    if submitted:
        if not name or not uploaded_file:
            st.warning("Bitte gib deinen Namen ein und lade eine CSV-Datei hoch.")
        else:
            # CSV laden
            user_data = pd.read_csv(uploaded_file)

            # Daten in Session speichern
            st.session_state.main_data = user_data
            st.session_state.current_user = User(user_id=1, user_name=name, user_age=age)
            st.session_state.current_user.assign_user_data(user_data)

            # Zusatzdaten initialisieren
            st.session_state.strength_sessions, st.session_state.cardio_sessions, st.session_state.low_impact_sessions = set_sport_sessions("data/sport_sessions.csv")[1:]
            st.session_state.cycle_phases = set_cycle_phases()
            st.session_state.has_started = True
            st.success("Daten erfolgreich geladen!")

#%% Dashboard-Anzeige
if st.session_state.has_started and st.session_state.current_user:

    user = st.session_state.current_user
    current_phase = get_current_phase()
    current_cycle_day = get_current_cycle_day()
    colors = get_color_palette()

    # Begrüßung
    h1(f"{user.user_name}'s Phasely Dashboard")
    textblock("Willkommen zu deinem Phasely Dashboard! Hier bekommst du reichlich Infos über deine Zyklusphasen und die optimale Trainingsgestaltung während dieser Phasen.")
    st.markdown("---")

    # Aktuelle Phase
    h2(f"""Du bist in deiner <span style="color: {colors["Primary"]};">{current_phase.phase_name}</span>""")
    textblock(current_phase.description)

    with st.container():
        textblock(f"""<span style="font-weight:bold;">Heute ist dein {current_cycle_day}. Zyklustag!</span>""")
        colleft, col1, colright = st.columns([3, 6, 3])
        with col1:
            current_cycle_plot_2()

    # Verteilung
    h3("Optimale Trainingsverteilung")
    colleft, col1, col2, col3, col4, colright = st.columns(6)
    with col1:
        view_score_percentage(current_phase.strength_score, "Krafttraining", colors["Primary"])
    with col2:
        view_score_percentage(current_phase.cardio_score, "Ausdauertraining", colors["Primary"])
    with col3:
        view_score_percentage(current_phase.low_impact_score, "Low-Impact", colors["Primary"])
    with col4:
        st.markdown(f"""
            <div style="text-align: center; font-family: 'Inter', sans-serif;">
                <div style="font-size: 40px; font-weight: bold; color: #834F34; margin-top: 20px;">
                    {int(min(current_phase.training_intensity) * 100)} - {int(max(current_phase.training_intensity) * 100)}%
                </div>
                <div style="margin-bottom: 8px;">Intensität</div>
            </div>
        """, unsafe_allow_html=True)

    # Info-Karten
    colleft, col1, col2, colright = st.columns([2, 4, 4, 2])
    with col1:
        info_card(
            "Warum zyklusbasiertes Training?",
            "Dein Zyklus beeinflusst Energie, Belastbarkeit und Regeneration. Ein Training, das auf deine jeweilige Phase abgestimmt ist, kann effektiver, nachhaltiger und angenehmer sein."
        )
    with col2:
        info_card(
            "Wie funktioniert das?",
            "Je nach Phase verändern sich deine Hormone. Phasely erkennt diese Veränderungen anhand deiner Daten und gibt passende Trainingsempfehlungen."
        )

    st.markdown("---")
    h2("Erstelle dein zyklusbasiertes Training")

    colleft, col1, colright = st.columns(3)
    with col1:
        button("show_trainingsplanung", "✨ Zyklusbasierte Trainingswoche erstellen ✨")

    if st.session_state["show_trainingsplanung"]:
        show_selection()
        show_match_scores()
