import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from streamlit_sortables import sort_items
from streamlit import experimental_rerun
from src.calculations import calculate_scores_complex, calculate_match_score_simple
from src.interface_components import h1, h2, h3, textblock, h_divider, view_score_percentage, info_card, button, button_close, button_toggle

def show_match_score(selected_sessions):
    final_score, final_strength_score, final_cardio_score, final_low_impact_score = calculate_scores_complex(selected_sessions)

    h2("Deine Scores")

    view_score_percentage(final_score, "Gesamtscore")