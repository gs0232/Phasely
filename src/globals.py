from src.data_setup import load_data, set_sport_sessions, set_cycle_phases
from src.classes import User
import pandas as pd

MAIN_FILE_PATH = "data/cycle_tracking_2025.csv"
SPORT_SESSIONS_PATH = "data/sport_sessions.csv"

main_data = load_data(MAIN_FILE_PATH)
sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions = set_sport_sessions(SPORT_SESSIONS_PATH)
cycle_phases = set_cycle_phases()

first_future_index = main_data[main_data["is_historic"] == False].index[0]
current_index = first_future_index - 1

current_user = User(1, "Heidi", 22)
current_user.assign_user_data(main_data)

current_phase_name = main_data["phase"].iloc[current_index]
for i in cycle_phases:
    if i.phase_name == current_phase_name:
        current_phase = i
        break

colors = {
    "Primary": "#CB997E",
    "Primary-light": "#DDBEA9",
    "Secondary": "#6B705C",
    "Secondary-light": "#A7AC9A",
    "Highlight": "#6665DD",
    "Highlight-light": "#9B9ECE"
}