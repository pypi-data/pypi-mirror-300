import os
import json
import shap
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor
from sklearn.linear_model import LinearRegression

def feature_importance_drift(label, mode, model, buffer, X,y = None, exclusions=[]):
    """
    A function to track feature importance drift and direction (positive or negative impact) using SHAP.
    
    Args:
        label (str): A text label for the dataset.
        mode (str): 'training' or 'scoring'. In 'training' mode, it saves SHAP values for feature importance 
                    and direction. In 'scoring' mode, it compares the current SHAP values with stored values.
        model (object): The trained machine learning model (e.g., RandomForest, XGBoost, Linear Regression).
        df (pd.DataFrame): The input DataFrame (without the target column in scoring mode).
        buffer (str): The path to store or load SHAP values for feature importance and direction.
        target_column (str): Name of the target column (required in training mode).
        exclusions (list): List of columns to exclude from analysis.

    Note: Supports RandomForest, XGBoost, Linear Regression only. 
        
    Returns:
        None: Saves or compares feature importance and direction.
    """

    feature_cols = [col for col in X.columns if col not in exclusions]
    
    buffer_path = os.path.join(buffer, f"{label}_shap_values.json")   
    
    if isinstance(model, (RandomForestClassifier, RandomForestRegressor)):
        explainer = shap.TreeExplainer(model)
    elif isinstance(model, (XGBClassifier, XGBRegressor)):
        explainer = shap.TreeExplainer(model)
    elif isinstance(model, LinearRegression):
        explainer = shap.LinearExplainer(model, df[feature_cols])
    else:
        raise ValueError("Unsupported model type. Supported types: RandomForest, XGBoost, Linear Regression.")
    
    if mode == 'training':
        if y is None:
            raise ValueError("Target column is required in training mode.")

        if os.path.exists(buffer_path):
            raise FileExistsError(f"A file with label '{label}' already exists in the buffer. Overwriting is not allowed.")
        
        X_train = X
        y_train = y
                
        shap_values = explainer.shap_values(X_train)
        shap_summary = {
            "feature_importance": np.mean(np.abs(shap_values), axis=0).tolist(),
            "features": feature_cols
        }
        
        with open(buffer_path, 'w') as f:
            json.dump(shap_summary, f)
        
        print(f"SHAP values for feature importance and direction saved to {buffer_path}.")
    
    elif mode == 'scoring':
        if not os.path.exists(buffer_path):
            raise FileNotFoundError(f"SHAP values not found at {buffer_path}. Please run in 'training' mode first.")
        
        with open(buffer_path, 'r') as f:
            shap_summary_training = json.load(f)
        
        X_scoring = X
        
        shap_values_scoring = explainer.shap_values(X_scoring)
        shap_summary_scoring = {
            "feature_importance": np.mean(np.abs(shap_values_scoring), axis=0).tolist(),
            "features": feature_cols
        }
        
        drift_detected = False
        print("Feature Importance Drift Check:")

        print(len(shap_summary_training['features']))
        
        for i, feature in enumerate(shap_summary_training['features']):
            importance_diff = abs(shap_summary_scoring['feature_importance'][i] - shap_summary_training['feature_importance'][i])
            
            if importance_diff > 0.05 * shap_summary_training['feature_importance'][i]:
                drift_detected = True
                print(f"  - {feature}: Significant change in feature importance (Training: {shap_summary_training['feature_importance'][i]:.4f}, Scoring: {shap_summary_scoring['feature_importance'][i]:.4f}).")
            
        if not drift_detected:
            print("No feature importance drift detected.")
    
    else:
        raise ValueError("Invalid mode. Choose either 'training' or 'scoring'.")
