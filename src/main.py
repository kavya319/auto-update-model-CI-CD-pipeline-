# src/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# 1. Load the model ONCE when the app starts
try:
    model = joblib.load("model/v1.pkl")
    print("Model loaded successfully.")
except:
    print("Model not found. Run train.py first!")
    model = None

# Define input data structure
class InputData(BaseModel):
    hours_studied: float

@app.get("/")
def home():
    return {"message": "ML Service is Running!"}

@app.post("/predict")
def predict(data: InputData):
    if not model:
        return {"error": "Model is not trained yet."}
    
    # Make prediction
    input_array = np.array([[data.hours_studied]])
    prediction = model.predict(input_array)
    
    return {
        "hours": data.hours_studied,
        "predicted_score": prediction[0]
    }