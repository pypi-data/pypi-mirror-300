import os

def delete_drift_dump(label, buffer):
    """
    A function to delete a distinct values dump file from the buffer.

    Args:
        label (str): A text label for the dataset.
        buffer (str): Path to the buffer directory where the file is stored.

    Returns:
        None: Deletes the file if it exists, otherwise raises a FileNotFoundError.
    """
    
    buffer_path = os.path.join(buffer, f"{label}_distinct_values.json")
    
    if os.path.exists(buffer_path):
        os.remove(buffer_path)
        print(f"File '{buffer_path}' has been deleted successfully.")
    else:
        raise FileNotFoundError(f"No file found with label '{label}' in the buffer.")
