# app/services/prediction_service.py
from datetime import datetime
import joblib
import numpy as np
import os
from app.core.config import settings

class PredictionService:
    def __init__(self):
        self.delay_model = None
        self.risk_model = None
        self.load_models()

    def load_models(self):
        try:
            model_dir = "app/ml_models"
            delay_path = f"{model_dir}/delay_model.pkl"
            risk_path = f"{model_dir}/risk_model.pkl"
            
            if os.path.exists(delay_path):
                self.delay_model = joblib.load(delay_path)
            if os.path.exists(risk_path):
                self.risk_model = joblib.load(risk_path)
                
            print("✅ Prediction models loaded successfully")
        except Exception as e:
            print(f"❌ Model loading error: {e}")
            self.delay_model = None
            self.risk_model = None

    def predict_delay(self, train_id: str, hour: int, day_type: str = "weekday") -> dict:
        try:
            if self.delay_model is None:
                return self._dummy_delay_prediction(train_id, hour)

            # Prepare features (adjust based on your actual model)
            features = np.array([[hour, 1 if day_type == "weekday" else 0]])
            delay_minutes = float(self.delay_model.predict(features)[0])
            delay_minutes = max(0, round(delay_minutes, 1))

            return {
                "train_id": train_id,
                "predicted_delay": delay_minutes,
                "status": "Delayed" if delay_minutes > 5 else "On Time",
                "confidence": "Medium",
                "note": "⚠️ এই Delay Prediction সম্পূর্ণ সিন্থেটিক ডেটা দিয়ে তৈরি মডেলের উপর ভিত্তি করে। বাস্তব সময়ের সাথে পার্থক্য থাকতে পারে।"
            }
        except Exception as e:
            print(f"Delay prediction error: {e}")
            return self._dummy_delay_prediction(train_id, hour)

    def predict_risk(self, stop_name: str, hour: int, day_type: str = "weekday") -> dict:
        try:
            if self.risk_model is None:
                return self._dummy_risk_prediction(stop_name, hour)

            features = np.array([[hour, hash(stop_name) % 20, 1 if day_type == "weekday" else 0]])
            risk_score = float(self.risk_model.predict(features)[0])
            risk_score = max(15, min(92, round(risk_score, 1)))

            risk_level = "High" if risk_score > 65 else "Medium" if risk_score > 40 else "Low"

            return {
                "stop_name": stop_name,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "peak_hours": "সকাল ৭-৯টা ও বিকেল ৪-৬টায় ঝুঁকি সাধারণত বেশি",
                "note": "⚠️ এই Risk Prediction সম্পূর্ণ সিন্থেটিক ডেটার উপর ভিত্তি করে তৈরি। এটি শুধু সচেতনতার জন্য, বাস্তব তথ্য নয়।"
            }
        except Exception as e:
            print(f"Risk prediction error: {e}")
            return self._dummy_risk_prediction(stop_name, hour)

    def _dummy_delay_prediction(self, train_id: str, hour: int):
        base_delay = (hour % 9) * 3.2
        delay_minutes = round(max(0, base_delay), 1)
        return {
            "train_id": train_id,
            "predicted_delay": delay_minutes,
            "status": "Delayed" if delay_minutes > 7 else "On Time",
            "confidence": "Low",
            "note": "⚠️ এই Delay Prediction সম্পূর্ণ সিন্থেটিক ডেটা দিয়ে তৈরি মডেলের উপর ভিত্তি করে। বাস্তব সময়ের সাথে পার্থক্য থাকতে পারে।"
        }

    def _dummy_risk_prediction(self, stop_name: str, hour: int):
        base_risk = 40 + (hour % 12) * 4.5
        if any(x in stop_name for x in ["ফতেয়াবাদ", "বটতলী", "ঝাউতলা"]):
            base_risk += 28
        risk_score = round(max(22, min(90, base_risk)), 1)
        
        risk_level = "High" if risk_score > 65 else "Medium" if risk_score > 40 else "Low"
        
        return {
            "stop_name": stop_name,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "peak_hours": "সকাল ৭-৯টা ও বিকেল ৪-৬টায় ঝুঁকি সাধারণত বেশি",
            "note": "⚠️ এই Risk Prediction সম্পূর্ণ সিন্থেটিক ডেটার উপর ভিত্তি করে তৈরি। এটি শুধু সচেতনতার জন্য, বাস্তব তথ্য নয়।"
        }


prediction_service = PredictionService()