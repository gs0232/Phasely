#%% Import
from src.data_setup import load_data, set_sport_sessions, set_cycle_phases
from src.classes import User
from src.calculations import calculate_scores_complex, calculate_match_score_simple
import pandas as pd
import plotly.express as px
import numpy as np

#%% Set data
MAIN_FILE_PATH = "data/cycle_tracking_2025.csv"
SPORT_SESSIONS_PATH = "data/sport_sessions.csv"

main_data = load_data(MAIN_FILE_PATH)
sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions = set_sport_sessions(SPORT_SESSIONS_PATH)
cycle_phases = set_cycle_phases()

first_future_index = main_data[main_data["is_historic"] == False].index[0]
current_index = first_future_index - 1

print(current_index)


#%% Initialzie User and current phase
current_user = User(1, "Heidi", 22)
current_user.assign_user_data(main_data)

current_phase_name = main_data["phase"].iloc[current_index]

for i in cycle_phases:
    if i.phase_name == current_phase_name:
        current_phase = i
        break

# %%
selected_sport = cardio_sessions[3]  # Example: select the first strength session

match_score = calculate_match_score_simple(selected_sport, current_phase, main_data, current_index)
print(f"Match score for {selected_sport.session_name} in {current_phase.phase_name}: {match_score * 100}%")

#%% Complex Calculation

sport_sessions[0].select_session("selected")
sport_sessions[1].select_session("selected")
sport_sessions[2].select_session("selected")

final_score, final_strength_score, final_cardio_score, final_low_impact_score = calculate_scores_complex(sport_sessions, current_phase, main_data, current_index)
print(f"Der finale Kraft-Score ist: {final_strength_score *100}%")
print(f"Der finale Ausdauer-Score ist: {final_cardio_score *100}%")
print(f"Der finale Low-Impact-Score ist: {final_low_impact_score *100}%")

print(f"Der Gesamtscore ist: {final_score *100}%")

# %%
