#%%
import pandas as pd

class User():
    
    def __init__(self, user_id, user_name, user_age): 
        """
        Initialize a User object
        """
        self.user_id = user_id
        self.user_name = user_name
        self.user_ager = user_age

    def assign_user_data(self, data):
        """
        Set the main data for the user
        """
        self.data = data

    def __str__(self):
        """
        String representation of the User object
        """
        return f"User ID: {self.user_id}, Name: {self.user_name}, Age: {self.user_age}"

class CyclePhase():
    def __init__(self, phase_name, training_intensity, strength_score, cardio_score, low_impact_score, description):
        """
        Initialize a CyclePhase object
        """
        self.phase_name = phase_name
        self.training_intensity = training_intensity
        self.strength_score = strength_score
        self.cardio_score = cardio_score
        self.low_impact_score = low_impact_score
        self.description = description

    def __str__(self):
        """
        String representation of the CyclePhase object
        """
        return (f"Cycle Phase: {self.phase_name}, "
                f"Training Intensity: {self.training_intensity}, "
                f"Strength Score: {self.strength_score}, "
                f"Cardio Score: {self.cardio_score}, "
                f"Low Impact Score: {self.low_impact_score}")
    

class SportSession():
    def __init__(self, session_name, category, duration, intensity, strength_score, cardio_score, low_impact_score, is_selected):
        """
        Initialize a SportSessions object
        """
        self.session_name = session_name
        self.category = category
        self.duration = duration
        self.intensity = intensity
        self.strength_score = strength_score
        self.cardio_score = cardio_score
        self.low_impact_score = low_impact_score
        self.is_selected = is_selected


    def __str__(self):
        """
        String representation of the SportSessions object
        """
        return (f"Session Name: {self.session_name}, "
                f"Duration: {self.duration}, "
                f"Intensity: {self.intensity}, "
                f"Strength Score: {self.strength_score}, "
                f"Cardio Score: {self.cardio_score}, "
                f"Low Impact Score: {self.low_impact_score}")
    

# %%
