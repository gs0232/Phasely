import pandas as pd

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
    
def calculate_match_score(sport, phase, main_data, current_index):
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