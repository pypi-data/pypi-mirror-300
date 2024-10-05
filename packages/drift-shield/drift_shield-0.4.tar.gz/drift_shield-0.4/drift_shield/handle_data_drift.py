import os
import pandas as pd
import json

def handle_data_drift(label, df, buffer, default_replacements, exclusions=[]):
    """
    A function to handle data drift by detecting drift and replacing drifted values 
    with defaults from a given DataFrame.

    Args:
        label (str): A text label for the dataset.
        df (pd.DataFrame): The DataFrame to analyze.
        buffer (str): Path to store/load the distinct values.
        default_replacements (pd.DataFrame): A DataFrame containing default values to replace drifted values.
        exclusions (list): List of columns to exclude from analysis.

    Returns:
        pd.DataFrame: Updated DataFrame with drifted values replaced.
    """
    df_new = df.copy()
    buffer_path = os.path.join(buffer, f"{label}_distinct_values.json")
    
    if not os.path.exists(buffer_path):
        raise FileNotFoundError(f"Buffer file not found at {buffer_path}. Please run in 'training' mode first.")
    
    with open(buffer_path, 'r') as f:
        distinct_values_training = json.load(f)
    
    distinct_values_training = distinct_values_training.get('distinct_values', {})
    drift_detected = False

    for col, distinct_training_vals in distinct_values_training.items():
        if col not in df.columns:
            print(f"Warning: Column '{col}' found in buffer but not in scoring DataFrame.")
            continue
        
        if col in exclusions:
            print(f"Excluding column '{col}' from drift detection.")
            continue
        
        distinct_values_scoring = df[col].unique().tolist()
        
        new_values = set(distinct_values_scoring) - set(distinct_training_vals)

        if new_values:
            drift_detected = True
            print(f"Data drift detected in column '{col}': New values - {new_values}")
            
            for new_val in new_values:
                if col in default_replacements.columns:
                    default_val = default_replacements.at[0, col]
                    print(f"Replacing '{new_val}' in column '{col}' with default '{default_val}'.")
                    df_new[col].replace(new_val, default_val, inplace=True)
                else:
                    print(f"No default replacement found for column '{col}', keeping original values.")
    
    if not drift_detected:
        print("No data drift detected.")
    
    return df_new