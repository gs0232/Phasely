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