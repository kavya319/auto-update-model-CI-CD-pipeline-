# src/add_data.py
"""
Utility script to add new user data
This simulates real users submitting data to the system
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime
from data_manager import increment_data_count, get_data_count
from config import NEW_DATA_DIR


def add_single_dataset(hours_studied, score):
    """
    Add a single user dataset
    
    Args:
        hours_studied: Number of hours studied
        score: Score achieved
    """
    # Create a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"user_data_{timestamp}.csv"
    filepath = os.path.join(NEW_DATA_DIR, filename)
    
    # Create dataframe with single row
    df = pd.DataFrame({
        'hours_studied': [hours_studied],
        'score': [score]
    })
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    
    # Increment counter
    count = increment_data_count(1)
    
    print(f"[OK] Added new dataset: {hours_studied} hours -> {score} score")
    print(f"[DATA] Total new datasets: {count}/200")
    
    return count


def add_multiple_datasets(num_datasets):
    """
    Add multiple simulated datasets for testing
    
    Args:
        num_datasets: Number of datasets to generate
    """
    print(f"Generating {num_datasets} simulated datasets...")
    
    for i in range(num_datasets):
        # Generate realistic data with some noise
        # Base relationship: score ≈ 10 * hours_studied + noise
        hours = np.random.uniform(1, 10)
        base_score = 10 * hours
        noise = np.random.normal(0, 5)  # Add some randomness
        score = base_score + noise
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"user_data_{timestamp}_{i}.csv"
        filepath = os.path.join(NEW_DATA_DIR, filename)
        
        # Create dataframe
        df = pd.DataFrame({
            'hours_studied': [hours],
            'score': [score]
        })
        
        # Save to CSV
        df.to_csv(filepath, index=False)
    
    # Increment counter once for all datasets
    count = increment_data_count(num_datasets)
    
    print(f"[OK] Added {num_datasets} new datasets")
    print(f"Total new datasets: {count}/200")
    
    return count


def check_status():
    """Check the current status of new data"""
    count = get_data_count()
    print(f"\n{'='*50}")
    print(f"New Datasets Status")
    print(f"{'='*50}")
    print(f"Current count: {count}")
    print(f"Threshold: 200")
    print(f"Progress: {(count/200)*100:.1f}%")
    
    if count >= 200:
        print("[OK] Ready for retraining!")
    else:
        print(f"[WAIT] Need {200-count} more datasets")
    print(f"{'='*50}\n")
    
    return count


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Usage: python add_data.py <number_of_datasets>
        num = int(sys.argv[1])
        add_multiple_datasets(num)
    else:
        # Default: add a few sample datasets
        print("Adding 5 sample datasets...")
        add_multiple_datasets(5)
    
    check_status()
