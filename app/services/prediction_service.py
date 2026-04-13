# app/services/prediction_service.py
import joblib
import pandas as pd
import json
import os
from fastapi import HTTPException
from app.core.config import settings

class PredictionService:
    def __init__(self):
        self.models = {}
        self.columns = {}
        self.delay_cols = []
        self.risk_cols = []
        self.incident_cols = []
        self.load_models()

    def load_models(self):
        model_dir = settings.MODEL_DIR
        try:
            self.models["delay"] = joblib.load(f"{model_dir}/delay_model.pkl")
            self.models["incident"] = joblib.load(f"{model_dir}/incident_model.pkl")
            self.models["risk"] = joblib.load(f"{model_dir}/risk_model.pkl")
            print("✅ All ML models loaded successfully")
        except Exception as e:
            print(f"❌ MODEL LOAD ERROR: {e}")

        try:
            with open(f"{model_dir}/columns.json") as f:
                self.columns = json.load(f)
            print("✅ Columns mapping loaded")
        except Exception as e:
            print(f"⚠️ COLUMN LOAD ERROR: {e}")

        self.delay_cols = self.columns.copy()
        self.risk_cols = self.columns.copy()
        self.incident_cols = self.columns.copy()

    def prepare_input(self, data: dict, feature_columns: list):
        try:
            df = pd.DataFrame([data])
            df = pd.get_dummies(df)
            for col in feature_columns:
                if col not in df.columns:
                    df[col] = 0
            df = df[feature_columns]
            return df
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Input preparation error: {str(e)}")


prediction_service = PredictionService()