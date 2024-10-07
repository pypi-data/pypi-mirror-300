import os
import pandas as pd
import json
from scipy import stats

def data_drift(label, mode, df, buffer, exclusions=[], debugging_mode = 0):
    """
    A function to detect data drift in both non-numeric (distinct value changes) 
    and numeric/boolean (mean comparison) columns.

    Args:
        label (str): A text label for the dataset.
        mode (str): 'training' or 'scoring'. In 'training' mode, saves distinct values for non-numeric columns 
                    and means for numeric/boolean columns. In 'scoring' mode, compares current values with those
                    saved during training.
        df (pd.DataFrame): The DataFrame to analyze.
        buffer (str): Path to store/load the distinct values and statistics.
        exclusions (list): List of columns to exclude from analysis.

    Returns:
        None: In training mode, saves values. In scoring mode, prints any drift detected.
    """
    def remove_outliers(series):
        """Removes outliers using the IQR method."""
        q25, q75 = series.quantile(0.25), series.quantile(0.75)
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        return series[(series >= lower_bound) & (series <= upper_bound)]

    
    buffer_path = os.path.join(buffer, f"{label}_distinct_values.json")
    
    if mode == 'training':
        non_numeric_cols = df.select_dtypes(exclude=['number', 'bool', 'datetime']).columns
        non_numeric_cols = [col for col in non_numeric_cols if col not in exclusions]
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        numeric_cols = [col for col in numeric_cols if col not in exclusions]

        boolean_cols = df.select_dtypes(include=['bool']).columns
        boolean_cols = [col for col in boolean_cols if col not in exclusions]
        
        distinct_values = {col: df[col].unique().tolist() for col in non_numeric_cols}

        numeric_stats = {}
        for col in numeric_cols:
            df_no_outliers = remove_outliers(df[col]) 
            numeric_stats[col] = {'mean': df_no_outliers.mean(), 
                               'n': len(df[col]), 
                               'std' : df[col].std(), 
                               '25th': df[col].quantile(0.25),
                               '50th': df[col].quantile(0.50),
                               '75th': df[col].quantile(0.75)}
        
        boolean_stats = {col: {'proportion_true': df[col].mean(), 'n': len(df[col])} for col in boolean_cols}

        data_to_save = {
            'distinct_values': distinct_values,
            'numeric_stats': numeric_stats,
            'boolean_stats': boolean_stats
        }
        

        if debugging_mode:
            print(distinct_values)
            print(numeric_stats)
            print(boolean_stats)
        
        if os.path.exists(buffer_path):
            raise FileExistsError(f"A file with label '{label}' already exists in the buffer. Overwriting is not allowed.")
        
        with open(buffer_path, 'w') as f:
            json.dump(data_to_save, f)
        
        print(f"Distinct values and numeric statistics saved to {buffer_path}")
    
    elif mode == 'scoring':
        if not os.path.exists(buffer_path):
            raise FileNotFoundError(f"Buffer file not found at {buffer_path}. Please run in 'training' mode first.")
        
        with open(buffer_path, 'r') as f:
            data_from_training = json.load(f)
        
        distinct_values_training = data_from_training.get('distinct_values', {})
        numeric_stats_training = data_from_training.get('numeric_stats', {})
        boolean_stats_training = data_from_training.get('boolean_stats', {})

        drift_detected = False
        
        for col, distinct_training_vals in distinct_values_training.items():
            if col not in df.columns:
                print(f"Warning: Column '{col}' found in buffer but not in scoring DataFrame.")
                continue
            
            if col in exclusions:
                print(f"Excluding column '{col}' from drift detection.")
                continue
            
            distinct_values_scoring = df[col].unique().tolist()
            if set(distinct_values_scoring) != set(distinct_training_vals):
                new_values = set(distinct_values_scoring) - set(distinct_training_vals)
                if new_values:
                    drift_detected = True
                    print(f"Data drift detected in column '{col}': New values - {new_values}")

        for col, stats_training in numeric_stats_training.items():
            if col not in df.columns:
                print(f"Warning: Column '{col}' found in buffer but not in scoring DataFrame.")
                continue
            
            if col in exclusions:
                print(f"Excluding column '{col}' from drift detection.")
                continue

            df_no_outliers = remove_outliers(df[col])
            mean_scoring = df_no_outliers.mean()
            n_scoring = len(df[col])
            std_scoring = df[col].std()
            p25_scoring = df[col].quantile(0.25)
            p50_scoring = df[col].quantile(0.50)
            p75_scoring = df[col].quantile(0.75)


            mean_training = stats_training['mean']
            std_training = stats_training['std']
            n_training = stats_training['n']
            p25_training = stats_training['25th']
            p50_training = stats_training['50th']
            p75_training = stats_training['75th']           

            if debugging_mode:
                pass
                # print(mean_scoring)
                # print(n_scoring)
            
            t_stat, p_value = stats.ttest_ind_from_stats(
                mean1=mean_training, std1=std_training, nobs1=n_training,
                mean2=mean_scoring, std2=std_scoring, nobs2=n_scoring, equal_var=False
            )
            
            # Check if the difference in percentiles or mean is statistically significant
            if (abs(p25_scoring - p25_training) > 0.05 * p25_training or
                abs(p50_scoring - p50_training) > 0.05 * p50_training or
                abs(p75_scoring - p75_training) > 0.05 * p75_training or
                p_value < 0.05):
                
                drift_detected = True
                print(f"Data drift detected in numeric/boolean column '{col}': Statistically significant difference in mean or percentiles")
                print(f"Training vs Scoring statistics for '{col}':")
                print(f"  Mean - Training: {mean_training}, Scoring: {mean_scoring}")
                print(f"  25th percentile - Training: {p25_training}, Scoring: {p25_scoring}")
                print(f"  50th percentile - Training: {p50_training}, Scoring: {p50_scoring}")
                print(f"  75th percentile - Training: {p75_training}, Scoring: {p75_scoring}")
        
        if not drift_detected:
            print("No data drift detected.")

 # Check drift for boolean columns
        for col, stats_training in boolean_stats_training.items():
            if col not in df.columns:
                print(f"Warning: Column '{col}' found in buffer but not in scoring DataFrame.")
                continue
            
            if col in exclusions:
                print(f"Excluding column '{col}' from drift detection.")
                continue
            
            proportion_true_scoring = df[col].mean()
            proportion_true_training = stats_training['proportion_true']
            
            if abs(proportion_true_scoring - proportion_true_training) > 0.05:
                drift_detected = True
                print(f"Data drift detected in boolean column '{col}': Significant change in proportion of True values.")
        
        if not drift_detected:
            print("No data drift detected.")
    
    else:
        raise ValueError("Invalid mode. Choose either 'training' or 'scoring'.")