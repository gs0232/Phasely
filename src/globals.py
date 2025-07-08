"""
globals.py

Globale Variablen und Initialisierungen für die Phasely App.
Lädt einmalig Daten, User, Trainingsphasen und Farben für die App.
"""

import pandas as pd
from src.data_setup import load_data, set_sport_sessions, set_cycle_phases
from src.classes import User

#%% Dateipfade zu den CSV-Dateien
MAIN_FILE_PATH = "data/cycle_tracking_2025.csv"
SPORT_SESSIONS_PATH = "data/sport_sessions.csv"

#%% Zyklusdaten laden
main_data = load_data(MAIN_FILE_PATH)

#%% Sporteinheiten laden und nach Kategorie aufteilen
sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions = set_sport_sessions(SPORT_SESSIONS_PATH)

#%% Zyklusphasen definieren
cycle_phases = set_cycle_phases()

#%% Aktuellen Index im Zyklus bestimmen (letzter vergangener Tag)
first_future_index = main_data[main_data["is_historic"] == False].index[0]
current_index = first_future_index - 1

#%% User-Objekt erstellen
current_user = User(1, "Heidi", 22)
current_user.assign_user_data(main_data)

#%% Aktuelle Phase ermitteln (CyclePhase-Objekt)
current_phase_name = main_data["phase"].iloc[current_index]
for i in cycle_phases:
    if i.phase_name == current_phase_name:
        current_phase = i
        break

#%% Aktueller Zyklustag
current_cycle_day = int(main_data["cycle_day"].iloc[current_index])

#%% Farbschema der App
colors = {
    "Primary": "#CB997E",
    "Primary-light": "#DDBEA9",
    "Secondary": "#6B705C",
    "Secondary-light": "#A7AC9A",
    "Highlight": "#6665DD",
    "Highlight-light": "#9B9ECE"
}
