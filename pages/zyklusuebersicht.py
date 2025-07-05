import streamlit as st
from src.globals import (
    MAIN_FILE_PATH, SPORT_SESSIONS_PATH, main_data,
    sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions,
    cycle_phases, current_index, current_user, current_phase
)
import pandas as pd

def show_zyklusuebersicht():
    st.markdown(f"""<h2>Dein Zyklus</h2>""")