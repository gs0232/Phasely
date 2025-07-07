#%%
import pandas as pd
import numpy as np
from src.classes import SportSession, CyclePhase

def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        main_data = pd.read_csv(file_path)
        return main_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
def set_sport_sessions(file_path):
    '''
    Load data form a CSV file and create arrays for all sessions and individual categories.

    Parameters:
    file_path (str): The path to the CSV file containing the sport sessions.

    Returns:
    sport_sessions: Array with Instances of the SportSession class
    strength_sessions: All Intances from the sport_sessions array in the category of strength sports.
    cardio_sessions: All Intances from the sport_sessions array in the category of cardio sports.
    low_impact_sessions: All Intances from the sport_sessions array in the category of low-impact sports.
    '''
    sport_sessions_data = pd.read_csv(file_path)

    sport_sessions = []

    for i in sport_sessions_data.iterrows():
        session = SportSession(
            session_name=i[1]["session_name"],
            category=i[1]["category"],
            duration=i[1]["duration"],
            intensity=i[1]["intensity"],
            strength_score=i[1]["strength_score"],
            cardio_score=i[1]["cardio_score"],
            low_impact_score=i[1]["low_impact_score"],
            is_selected=False
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

    return sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions

    def __str_(self):
        """
        String representation of the SportSession object.
        """
        return (f"Session Name: {self.session_name}, "
                f"Category: {self.category}, "
                f"Duration: {self.duration}, "
                f"Intensity: {self.intensity}, "
                f"Strength Score: {self.strength_score}, "
                f"Cardio Score: {self.cardio_score}, "
                f"Low Impact Score: {self.low_impact_score}, "
                f"Selected: {self.is_selected}")

def set_cycle_phases():
    '''
    Create objects for the four existing cycle phases.

    Returns:
    cycle_phases: Array with Intances of the CyclePhase class
    '''
    def inclusive_range(start, stop, step):
        """
        Gibt eine Liste von floats von start bis einschließlich stop mit gegebener Schrittweite zurück.
        """
        result = []
        current = start
        while current <= stop + 1e-9:  # kleiner Puffer wegen float-Rundungsfehler
            result.append(round(current, 10))  # 10 Stellen für saubere Werte
            current += step
        return result

    cycle_phases = [
        CyclePhase("Menstruation", inclusive_range(0.3, 0.6, 0.05), 0.2, 0.3, 0.5, 
                   "Der Hormonspiegel ist niedrig, der Körper arbeitet ökonomisch, benötigt aber mitunter mehr Ruhe. " \
                   "Leichte Bewegung wie Yoga, Spazieren oder lockeres Radfahren kann Krämpfe lindern und das Wohlbefinden steigern."),
        CyclePhase("Follikelphase", inclusive_range(0.6, 0.9, 0.05), 0.55, 0.35, 0.1, 
                   "Östrogen steigt an, die Energiebereitstellung ist effizient und die Regenerationsfähigkeit besonders hoch. " \
                   "Diese Phase eignet sich ideal für intensives Krafttraining, Ausdaueraufbau und Leistungssteigerung."),
        CyclePhase("Ovulation", inclusive_range(0.7, 1.0, 0.05), 0.5, 0.3, 0.2, 
                   "Östrogen erreicht seinen Höhepunkt, das zentrale Nervensystem ist leistungsfähig. " \
                   "Gleichzeitig sind Gelenke und Bänder etwas instabiler – Fokus auf Technik, Koordination und saubere Belastung."),
        CyclePhase("Lutealphase", inclusive_range(0.5, 0.75, 0.05), 0.25, 0.35, 0.4, 
                   "Progesteron dominiert, die Körpertemperatur ist erhöht und manche spüren mehr Fatigue. " \
                   "Diese Phase eignet sich gut für moderate Ausdauer, Mobility, funktionelles Krafttraining und Achtsamkeit.")
    ]

    return cycle_phases
# %%
