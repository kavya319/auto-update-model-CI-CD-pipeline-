# src/data_manager.py
"""
Data Manager Module
Handles loading, counting, and managing new user data for model retraining
"""
import json
import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime
from config import DATA_COUNTER_FILE, NEW_DATA_DIR


def get_data_count():
    """Get the current count of new datasets"""
    try:
        with open(DATA_COUNTER_FILE, 'r') as f:
            data = json.load(f)
            return data.get('count', 0)
    except FileNotFoundError:
        return 0


def increment_data_count(amount=1):
    """Increment the new data counter"""
    try:
        with open(DATA_COUNTER_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"count": 0, "last_trained": None, "current_version": 1}
    
    data['count'] += amount
    
    with open(DATA_COUNTER_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data count updated: {data['count']} new datasets")
    return data['count']


def reset_data_count():
    """Reset the data counter after training"""
    try:
        with open(DATA_COUNTER_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    data['count'] = 0
    data['last_trained'] = datetime.now().isoformat()
    
    with open(DATA_COUNTER_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Data counter reset after training")


def increment_version():
    """Increment the model version number"""
    try:
        with open(DATA_COUNTER_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"count": 0, "last_trained": None, "current_version": 1}
    
    data['current_version'] += 1
    
    with open(DATA_COUNTER_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    return data['current_version']


def get_current_version():
    """Get the current model version"""
    try:
        with open(DATA_COUNTER_FILE, 'r') as f:
            data = json.load(f)
            return data.get('current_version', 1)
    except FileNotFoundError:
        return 1


def load_new_data():
    """
    Load all new user data from the new_data directory
    Returns: X (features), y (targets) as numpy arrays
    """
    # Check if running in GitHub Actions (no CSV files in new_data)
    csv_files = glob.glob(os.path.join(NEW_DATA_DIR, "*.csv"))
    
    # Fallback to sample data if no real data (for GitHub Actions testing)
    if not csv_files:
        sample_dir = os.path.join(DATA_DIR, "new_data_sample")
        if os.path.exists(sample_dir):
            csv_files = glob.glob(os.path.join(sample_dir, "*.csv"))
            if csv_files:
                print(f"[INFO] Using sample data for testing...")
    
    if not csv_files:
        print("No new data found")
        return None, None
    
    print(f"Loading {len(csv_files)} new dataset files...")
    
    all_data = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            all_data.append(df)
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
    
    if not all_data:
        return None, None
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Assuming columns are 'hours_studied' and 'score'
    X = combined_df[['hours_studied']].values
    y = combined_df['score'].values
    
    print(f"Loaded {len(combined_df)} total data points from new datasets")
    
    return X, y


def clear_new_data():
    """Clear all CSV files from new_data directory after training"""
    csv_files = glob.glob(os.path.join(NEW_DATA_DIR, "*.csv"))
    
    for csv_file in csv_files:
        try:
            os.remove(csv_file)
            print(f"Removed: {csv_file}")
        except Exception as e:
            print(f"Error removing {csv_file}: {e}")
    
    print(f"Cleared {len(csv_files)} data files from new_data directory")


if __name__ == "__main__":
    # Test the data manager
    print(f"Current data count: {get_data_count()}")
    print(f"Current version: {get_current_version()}")
