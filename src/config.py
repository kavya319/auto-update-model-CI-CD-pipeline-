# src/config.py
"""
Configuration file for CI/CD ML Pipeline
Contains all constants and settings for the automated model training system
"""
import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data Configuration
NEW_DATA_THRESHOLD = 200  # Number of new datasets required to trigger retraining
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
NEW_DATA_DIR = os.path.join(DATA_DIR, "new_data")
DATA_COUNTER_FILE = os.path.join(DATA_DIR, "new_data_counter.json")

# Model Configuration
MODEL_DIR = os.path.join(PROJECT_ROOT, "model")
MODEL_METADATA_FILE = os.path.join(MODEL_DIR, "model_metadata.json")
CURRENT_MODEL_FILE = os.path.join(MODEL_DIR, "v1.pkl")

# Training Configuration
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Ensure directories exist
os.makedirs(NEW_DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
