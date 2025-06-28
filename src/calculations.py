
from src.data_setup import set_cycle_phases

def calculate_match_score_simple(sport, phase, main_data, current_index):
    """
    Calculate the match score between the selected sport session and a cycle phase.
    """
    inhaltlicher_score = (
        sport.strength_score * phase.strength_score +
        sport.cardio_score * phase.cardio_score +
        sport.low_impact_score * phase.low_impact_score
    ) / 3

    print(inhaltlicher_score)

    intensity_ratio = main_data["intensity_capacity"][current_index]
    print(intensity_ratio)
    if inhaltlicher_score > intensity_ratio:
        final_score = round(intensity_ratio / inhaltlicher_score, 2)
    elif inhaltlicher_score < intensity_ratio: 
        final_score = round(inhaltlicher_score / intensity_ratio, 2)
    return final_score

def calculate_scores_complex(sport_sessions, current_phase, main_data, current_index):
    """
    Calculate the intensity, strength, cardio, and low-impact score between multiple selected sport sessions and the current cycle phase.
    """
    selected_sessions = []
    each_general_score = []
    each_strength_score = []
    each_cardio_score = []
    each_low_impact_score = []

    for i in sport_sessions:
        if i.is_selected == True:
            selected_sessions.append(i)

    for j in selected_sessions:
        # General Score sollte schauen ob die intensity der session im rahmen der training_intensity der current_phase liegt.
        # Wenn ja, dann ist general_score = 1
        # Wenn nein, dann je größer die Abweichung desto geringer general_score... oder sogar als "gut", "mittel", "schlecht" 
        each_strength_score.append(j.strength_score)
        each_cardio_score.append(j.cardio_score)
        each_low_impact_score.append(j.low_impact_score)

    if len(each_strength_score) != 0:
        sessions_strength_score = (sum(each_strength_score) / len(each_strength_score))
        sessions_cardio_score = (sum(each_cardio_score) / len(each_cardio_score))
        sessions_low_impact_score = (sum(each_low_impact_score) / len(each_low_impact_score))

        if sessions_strength_score >= current_phase.strength_score:
            final_strength_score = round(current_phase.strength_score / sessions_strength_score, 2)
        else: 
            final_strength_score = round(sessions_strength_score / current_phase.strength_score, 2)

        if sessions_cardio_score >= current_phase.cardio_score:
            final_cardio_score = round(current_phase.cardio_score / sessions_cardio_score, 2)
        else: 
            final_cardio_score = round(sessions_cardio_score / current_phase.cardio_score, 2)

        if sessions_low_impact_score >= current_phase.low_impact_score:
            final_low_impacth_score = round(current_phase.low_impact_score / sessions_low_impact_score, 2)
        else: 
            final_low_impact_score = round(sessions_low_impact_score / current_phase.low_impact_score, 2)
    else:
        final_strength_score = 0
        final_cardio_score = 0
        final_low_impact_score = 0

    final_score = (
        final_strength_score / current_phase.strength_score +
        final_cardio_score / current_phase.cardio_score +
        final_low_impact_score / current_phase.low_impact_score
    ) / 3

    intensity_ratio = main_data["intensity_capacity"][current_index]

    #if sessions_intensity_score > intensity_ratio:
    #    final_intensity_score = round(intensity_ratio / sessions_intensity_score, 2)
    #elif sessions_intensity_score < intensity_ratio: 
    #    final_intensity_score = round(sessions_intensity_score / intensity_ratio, 2)

    #print(each_strength_score)
    #print(sessions_strength_score)
    #print(current_phase.strength_score)
    return final_score, final_strength_score, final_cardio_score, final_low_impact_score
