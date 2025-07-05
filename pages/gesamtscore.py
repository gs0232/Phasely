import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from streamlit_sortables import sort_items
from streamlit import experimental_rerun
from src.globals import (
    MAIN_FILE_PATH, SPORT_SESSIONS_PATH, main_data,
    sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions,
    cycle_phases, current_index, current_user, current_phase
)
from src.calculations import calculate_scores_complex, calculate_match_score_simple