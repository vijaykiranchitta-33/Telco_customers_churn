import joblib
import pandas as pd
from fastapi import FastAPI
from src.preprocessing import engineer_features

app = FastAPI(title="Telco Churn Prediction API")

model = joblib.load("models/voting_model.joblib")
model_columns = joblib.load("models/model_columns.joblib")

@app.post("/predict")
def predict(customer_data: dict):
    df = pd.DataFrame([customer_data])
    df = engineer_features(df)
    df_encoded = pd.get_dummies(df).reindex(columns=model_columns, fill_value=0)
    
    prob = model.predict_proba(df_encoded)[0][1]
    return {
        "churn_risk": "High" if prob > 0.5 else "Low",
        "probability": f"{round(prob * 100, 2)}%"
    }