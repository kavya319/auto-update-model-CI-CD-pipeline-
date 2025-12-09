# src/train.py
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os
import sys

# 1. Load Data (Simulating "New Data" coming from DB)
# In real life, fetch this from MongoDB
print("Fetching data...")
X = np.array([[1], [2], [3], [4], [5], [6], [7]]) # Added more data points
y = np.array([10, 20, 30, 40, 50, 60, 75]) # Slightly noisy data to make it interesting

# 2. Load Old Model (if exists) to compare
old_accuracy = 0
try:
    old_model = joblib.load("model/v1.pkl")
    old_preds = old_model.predict(X)
    old_mse = mean_squared_error(y, old_preds)
    # Convert MSE to a score (100 is perfect)
    old_accuracy = 100 - old_mse
    print(f"Current Model Accuracy Score: {old_accuracy:.2f}")
except:
    print("No existing model found. Comparison skipped.")
    old_accuracy = -9999

# 3. Train New Model
print("Training new candidate model...")
new_model = LinearRegression()
new_model.fit(X, y)
new_preds = new_model.predict(X)
new_mse = mean_squared_error(y, new_preds)
new_accuracy = 100 - new_mse
print(f"Candidate Model Accuracy Score: {new_accuracy:.2f}")

# 4. The Decision (Quality Gate)
if new_accuracy > old_accuracy:
    print("✅ Improvement detected! Saving new model...")
    os.makedirs("model", exist_ok=True)
    joblib.dump(new_model, "model/v1.pkl")
    
    # Write to a special file that GitHub Actions can read
    # This tells the YAML file: "Yes, create a PR"
    if os.getenv("GITHUB_ENV"):
        with open(os.getenv("GITHUB_ENV"), "a") as f:
            f.write("MODEL_CHANGED=true\n")
            f.write(f"ACCURACY={new_accuracy:.2f}\n")
else:
    print("❌ No improvement. Discarding candidate.")
    # Tell YAML not to bother
    if os.getenv("GITHUB_ENV"):
        with open(os.getenv("GITHUB_ENV"), "a") as f:
            f.write("MODEL_CHANGED=false\n")