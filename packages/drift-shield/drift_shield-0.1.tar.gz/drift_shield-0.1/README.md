# DriftShield

**DriftShield** is a Python package designed to detect and handle data drift in machine learning pipelines. It compares distributions of numeric and non-numeric data between training and scoring datasets, helps identify drift, and replaces problematic values with predefined defaults. With built-in outlier handling and statistical tests, **DriftShield** ensures that your data remains consistent and prevents performance degradation caused by unseen data changes.

## Features

- Detects data drift in non-numeric, numeric, and boolean columns.
- Handles outliers when calculating means for numeric data.
- Compares 25th, 50th, and 75th percentiles for numeric columns.
- Tracks changes in proportions for boolean columns.
- Provides mechanisms to replace drifted values with default values.
- Customizable exclusion of columns from drift detection.

## Installation

To install **DriftShield**, you can clone the repository and install it using `pip`:

```bash
git clone <>
cd driftshield
pip install .
```

Alternatively, you can install it directly from PyPI (after you’ve published it):

```bash
pip install driftshield
```

## Usage

**DriftShield** can be used to monitor and handle drift between training and scoring datasets. Here's a quick guide on how to use it:

### 1. Import the package

```python
from driftshield import data_drift, handle_data_drift
```

### 2. Detect Data Drift

In **training mode**, you can store distinct values and statistics for numeric/boolean columns.

```python
data_drift('my_dataset', 'training', training_df, './buffer_dir', exclusions=['column_to_exclude'])
```

In **scoring mode**, it will compare the statistics from the stored buffer to detect drift.

```python
data_drift('my_dataset', 'scoring', scoring_df, './buffer_dir', exclusions=['column_to_exclude'])
```

### 3. Handle Drift

If drift is detected, you can replace drifted values with values from a default DataFrame.

```python
updated_df = handle_data_drift('my_dataset', scoring_df, './buffer_dir', default_replacements_df, exclusions=['column_to_exclude'])
```

### 4. Delete Drift Dump

To remove a stored drift file if you need to reset or rerun:

```python
from driftshield import delete_drift_dump

delete_drift_dump('my_dataset', './buffer_dir')
```

## Example Workflow

1. **Training Phase:**
   - Store distinct values and statistics:
   ```python
   data_drift('my_training_data', 'training', training_df, './buffer')
   ```

2. **Scoring Phase:**
   - Compare scoring data to the training statistics:
   ```python
   data_drift('my_training_data', 'scoring', scoring_df, './buffer')
   ```

3. **Handling Drift:**
   - Replace drifted values with defaults:
   ```python
   updated_df = handle_data_drift('my_training_data', scoring_df, './buffer', default_replacements_df)
   ```