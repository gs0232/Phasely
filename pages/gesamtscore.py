import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from streamlit_sortables import sort_items
from streamlit import experimental_rerun
from src.interface_components import h2, view_score_percentage, info_card, button
from src.scores import calculate_match_scores
from src.globals import (current_phase)

def show_match_scores():
    selected_sessions = st.session_state.get("selected_sessions", [])
    if not selected_sessions:
        st.warning("Noch keine Sporteinheiten ausgewählt.")
        return
    
    df_scores, final_overall_score, final_strength_score, final_cardio_score, final_low_impact_score, text = calculate_match_scores(selected_sessions, current_phase)

    h2("Deine Trainingsverteilung")

    # Score-Anzeige in Spalten
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        view_score_percentage(final_overall_score, "Gesamt")
    with col2:
        view_score_percentage(final_strength_score, "Kraft")
    with col3:
        view_score_percentage(final_cardio_score, "Ausdauer")
    with col4:
        view_score_percentage(final_low_impact_score, "Low Impact")

    st.markdown("---")

    # Info-Cards für bestes & schlechtestes Workout
    '''col_best, col_worst = st.columns(2)

    with col_best:
        if best_session:
            info_card("Bestes Workout", f"**{best_session.session_name}** passt mit {int(round(best_session.match_score * 100))}% sehr gut zu deiner aktuellen Zyklusphase.")
        else:
            info_card("Bestes Workout", "–")

    with col_worst:
        if worst_session:
            info_card("Schlechtestes Workout", f"**{worst_session.session_name}** hat mit nur {int(round(worst_session.match_score * 100))}% eine geringe Passung zur aktuellen Zyklusphase.")
        else:
            info_card("Schlechtestes Workout", "–")'''

    st.markdown("---")

    # Tabelle mit Übersicht
    st.markdown("### 📋 Übersicht aller Einheiten")
    st.dataframe(df_scores)
