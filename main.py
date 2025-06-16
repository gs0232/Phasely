#%% Import
from src.data_setup import load_data, calculate_match_score
from src.classes import User, CyclePhase, SportSession
import pandas as pd
import plotly.express as px
import numpy as np

#%% Create CyclePhase objects
cycle_phases = [
    CyclePhase("Menstruation", np.arange(0, 0.2, 0.05), 0.35, 0.35, 1.0),
    CyclePhase("Follikelphase", np.arange(0.5, 0.9, 0.05), 1.0, 0.8, 0.5),
    CyclePhase("Ovulation", np.arange(0.9, 1.0, 0.05), 1.0, 1.0, 0.4),
    CyclePhase("Lutealphase", np.arange(0.4, 0.8, 0.05), 0.8, 1.0, 1.0)
]

#%% Initialize User and set data
main_data = load_data("data/cycle_tracking_2025.csv")

current_user = User(1, "Heidi", 22)
current_user.assign_user_data(main_data)

first_future_index = main_data[main_data["is_historic"] == False].index[0]
current_index = first_future_index - 1

current_phase_name = main_data["phase"].iloc[current_index]

for i in cycle_phases:
    if i.phase_name == current_phase_name:
        current_phase = i
        break

# %% Create SportSession objects
sport_sessions_data = pd.read_csv("data/sport_sessions.csv")

sport_sessions = []

for i in sport_sessions_data.iterrows():
    session = SportSession(
        session_name=i[1]["session_name"],
        category=i[1]["category"],
        duration=i[1]["duration"],
        intensity=i[1]["intensity"],
        strength_score=i[1]["strength_score"],
        cardio_score=i[1]["cardio_score"],
        low_impact_score=i[1]["low_impact_score"]
    )
    sport_sessions.append(session)

strength_sessions = []
cardio_sessions = []
low_impact_sessions = []

for i in sport_sessions:
    if i.category == "Kraftsport":
        strength_sessions.append(i)
    elif i.category == "Ausdauersport":
        cardio_sessions.append(i)
    elif i.category == "Low Impact":
        low_impact_sessions.append(i)

# %%
selected_sport = cardio_sessions[3]  # Example: select the first strength session

match_score = calculate_match_score(selected_sport, current_phase, main_data, current_index)
print(f"Match score for {selected_sport.session_name} in {current_phase.phase_name}: {match_score * 100}%")