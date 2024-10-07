import os
import json
from datetime import datetime

def monitor_data_volume_over_time(label, df, buffer, threshold=0.2):
    """
    A function to monitor data volume changes between successive scoring phases.
    
    Args:
        label (str): A text label for the dataset.
        df (pd.DataFrame): The input DataFrame to monitor.
        buffer (str): The path to store or load data volume information.
        threshold (float): The relative change threshold to flag data volume drift (default is 20%).
        log_file (str): File to track data volume across different scoring phases.
        
    Returns:
        None: Saves or compares data volume and prints drift alert if detected.
    """
    
    log_path = os.path.join(buffer, f"{label}_data_volume.json")
    
    volume_scoring = df.shape[0]
    
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            volume_log = json.load(f)
    else:
        volume_log = []
    
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    volume_log.append({
        "timestamp": current_timestamp,
        "volume_scoring": volume_scoring
    })
    
    with open(log_path, 'w') as f:
        json.dump(volume_log, f)
    
    print(f"Scoring data volume ({volume_scoring} samples) logged at {current_timestamp}.")
    
    if len(volume_log) > 1:
        previous_volume = volume_log[-2]["volume_scoring"]
        current_volume = volume_log[-1]["volume_scoring"]
        
        volume_change = abs(current_volume - previous_volume) / previous_volume
        
        print(f"Previous scoring volume: {previous_volume}, Current scoring volume: {current_volume}")
        
        if volume_change > threshold:
            print(f"Data volume drift detected between successive runs! The data volume has changed by {volume_change * 100:.2f}% compared to the previous run.")
        else:
            print(f"No significant data volume drift detected between successive runs. Volume change: {volume_change * 100:.2f}%.")
    else:
        print("No previous scoring phase to compare with.")

