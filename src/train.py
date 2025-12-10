# src/train.py
"""
Enhanced Training Script with Model Versioning and Comparison
This script:
1. Loads new user data from the new_data directory
2. Trains a new model version
3. Compares it with the current production model
4. Saves the new model if it performs better
5. Sets GitHub Actions environment variables for PR automation
"""
import joblib
import numpy as np
import json
import os
import sys
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_manager import (
    load_new_data, 
    reset_data_count, 
    get_current_version,
    increment_version,
    clear_new_data,
    get_data_count
)
from config import MODEL_DIR, MODEL_METADATA_FILE, RANDOM_STATE, TEST_SIZE


def save_model_metadata(version, accuracy, r2, mse, data_count):
    """Save model metadata to JSON file"""
    try:
        with open(MODEL_METADATA_FILE, 'r') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        metadata = {"models": []}
    
    model_info = {
        "version": version,
        "accuracy_score": round(accuracy, 4),
        "r2_score": round(r2, 4),
        "mse": round(mse, 4),
        "trained_at": datetime.now().isoformat(),
        "data_points": data_count
    }
    
    metadata["models"].append(model_info)
    
    with open(MODEL_METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"[OK] Saved metadata for model v{version}")


def load_current_model():
    """Load the current production model"""
    current_version = get_current_version()
    model_file = os.path.join(MODEL_DIR, f"v{current_version}.pkl")
    
    if os.path.exists(model_file):
        model = joblib.load(model_file)
        print(f"[OK] Loaded current model: v{current_version}")
        return model, current_version
    else:
        print("[WARNING] No existing model found")
        return None, 0


def evaluate_model(model, X, y):
    """Evaluate model performance"""
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    
    # Use R² score as accuracy metric (0-100 scale)
    # R² of 1.0 (perfect) = 100, R² of 0 (baseline) = 0
    accuracy = max(0, r2 * 100)
    
    return accuracy, r2, mse


def main():
    print("\n" + "="*60)
    print("[TRAINING] Starting Automated Model Training Pipeline")
    print("="*60 + "\n")
    
    # Check data count
    data_count = get_data_count()
    print(f"[DATA] New datasets available: {data_count}")
    
    if data_count < 200:
        print(f"[WARNING] Not enough data for training (need 200, have {data_count})")
        print("[SKIP] Skipping training")
        return
    
    # Step 1: Load new data
    print("\n[LOADING] Loading new user data...")
    X_new, y_new = load_new_data()
    
    if X_new is None or len(X_new) == 0:
        print("[ERROR] No new data found. Exiting.")
        return
    
    print(f"[OK] Loaded {len(X_new)} data points")
    
    # Step 2: Load current model for comparison
    print("\n[MODEL] Loading current production model...")
    current_model, current_version = load_current_model()
    
    # Step 3: Train new candidate model
    print("\n[TRAIN] Training new candidate model...")
    new_model = LinearRegression()
    
    # Split data for validation
    if len(X_new) > 10:
        X_train, X_test, y_train, y_test = train_test_split(
            X_new, y_new, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
    else:
        # If not enough data for split, use all for training and testing
        X_train, X_test, y_train, y_test = X_new, X_new, y_new, y_new
    
    new_model.fit(X_train, y_train)
    
    # Evaluate new model
    new_accuracy, new_r2, new_mse = evaluate_model(new_model, X_test, y_test)
    
    print(f"\n[METRICS] New Model Performance:")
    print(f"   Accuracy Score: {new_accuracy:.2f}%")
    print(f"   R2 Score: {new_r2:.4f}")
    print(f"   MSE: {new_mse:.4f}")
    
    # Step 4: Compare with current model
    old_accuracy = 0
    improved = False
    
    if current_model is not None:
        old_accuracy, old_r2, old_mse = evaluate_model(current_model, X_test, y_test)
        
        print(f"\n[CURRENT] Current Model Performance (v{current_version}):")
        print(f"   Accuracy Score: {old_accuracy:.2f}%")
        print(f"   R2 Score: {old_r2:.4f}")
        print(f"   MSE: {old_mse:.4f}")
        
        print(f"\n[COMPARE] Comparison:")
        accuracy_diff = new_accuracy - old_accuracy
        print(f"   Accuracy change: {accuracy_diff:+.2f}%")
        
        if new_accuracy > old_accuracy:
            improved = True
            print(f"   [SUCCESS] New model is BETTER!")
        else:
            print(f"   [FAIL] New model is NOT better")
    else:
        # No existing model, so any new model is an improvement
        improved = True
        print("\n[OK] First model - automatically accepted")
    
    # Step 5: Decision - Save or Discard
    if improved:
        # Increment version for new model
        new_version = increment_version()
        model_filename = f"v{new_version}.pkl"
        model_path = os.path.join(MODEL_DIR, model_filename)
        
        print(f"\n[SAVE] Saving new model as {model_filename}...")
        joblib.dump(new_model, model_path)
        
        # Save metadata
        save_model_metadata(new_version, new_accuracy, new_r2, new_mse, len(X_new))
        
        # Reset data counter and clear new data files
        reset_data_count()
        clear_new_data()
        
        # Set GitHub Actions environment variables
        if os.getenv("GITHUB_ENV"):
            with open(os.getenv("GITHUB_ENV"), "a") as f:
                f.write("MODEL_IMPROVED=true\n")
                f.write(f"NEW_VERSION={new_version}\n")
                f.write(f"NEW_ACCURACY={new_accuracy:.2f}\n")
                f.write(f"OLD_ACCURACY={old_accuracy:.2f}\n")
                f.write(f"OLD_VERSION={current_version}\n")
                f.write(f"MODEL_FILE={model_filename}\n")
            print("[OK] Set GitHub Actions environment variables")
        
        print(f"\n{'='*60}")
        print(f"[SUCCESS] Model v{new_version} saved and ready for deployment!")
        print(f"{'='*60}\n")
        
    else:
        print(f"\n{'='*60}")
        print("[NO IMPROVEMENT] New model did not improve performance")
        print("Model discarded - no changes made")
        print(f"{'='*60}\n")
        
        # Set GitHub Actions environment variable to skip PR
        if os.getenv("GITHUB_ENV"):
            with open(os.getenv("GITHUB_ENV"), "a") as f:
                f.write("MODEL_IMPROVED=false\n")
            print("[OK] Notified GitHub Actions - no PR will be created")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)