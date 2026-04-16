# app/services/prediction_service.py
import joblib
import numpy as np
import os
from fastapi import HTTPException

class PredictionService:
    def __init__(self):
        self.delay_model = None
        self.risk_model = None
        self.load_models()

    def load_models(self):
        try:
            model_dir = "app/ml_models"
            print(f"🔍 Looking for models in: {os.path.abspath(model_dir)}")
            
            delay_path = f"{model_dir}/delay_model.pkl"
            risk_path = f"{model_dir}/risk_model.pkl"
            
            if os.path.exists(delay_path):
                self.delay_model = joblib.load(delay_path)
                print("✅ Delay model loaded successfully")
            else:
                print(f"⚠️ Delay model not found at {delay_path}")
                
            if os.path.exists(risk_path):
                self.risk_model = joblib.load(risk_path)
                print("✅ Risk model loaded successfully")
            else:
                print(f"⚠️ Risk model not found at {risk_path}")
                
        except Exception as e:
            print(f"❌ Critical model loading error: {e}")

    def predict_delay(self, train_id: str, hour: int, day_type: str = "weekday"):
        try:
            if self.delay_model is None:
                print("⚠️ Using dummy delay prediction (model not loaded)")
                return self._dummy_delay_prediction(train_id, hour)

            features = np.array([[float(hour), 1 if day_type.lower() == "weekday" else 0]])
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
            print(f"❌ Delay prediction failed: {e}")
            return self._dummy_delay_prediction(train_id, hour)

    def predict_risk(self, stop_name: str, hour: int, day_type: str = "weekday"):
        try:
            if self.risk_model is None:
                print("⚠️ Using dummy risk prediction (model not loaded)")
                return self._dummy_risk_prediction(stop_name, hour)

            features = np.array([[float(hour), hash(stop_name) % 20, 1 if day_type.lower() == "weekday" else 0]])
            risk_score = float(self.risk_model.predict(features)[0])
            risk_score = max(15, min(92, round(risk_score, 1)))

            risk_level = "High" if risk_score > 65 else "Medium" if risk_score > 40 else "Low"

            return {
                "stop_name": stop_name,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "peak_hours": "সকাল ৭-৯টা ও বিকেল ৪-৬টায় ঝুঁকি বেশি",
                "note": "⚠️ এই Risk Prediction সম্পূর্ণ সিন্থেটিক ডেটার উপর ভিত্তি করে তৈরি। এটি শুধু সচেতনতার জন্য, বাস্তব তথ্য নয়।"
            }
        except Exception as e:
            print(f"❌ Risk prediction failed: {e}")
            return self._dummy_risk_prediction(stop_name, hour)

    def _dummy_delay_prediction(self, train_id: str, hour: int):
        delay_minutes = round((hour % 9) * 3.5, 1)
        return {
            "train_id": train_id,
            "predicted_delay": delay_minutes,
            "status": "Delayed" if delay_minutes > 8 else "On Time",
            "confidence": "Low",
            "note": "⚠️ এই Delay Prediction সম্পূর্ণ সিন্থেটিক ডেটা দিয়ে তৈরি মডেলের উপর ভিত্তি করে। বাস্তব সময়ের সাথে পার্থক্য থাকতে পারে।"
        }

    def _dummy_risk_prediction(self, stop_name: str, hour: int):
        base = 42 + (hour % 12) * 4.8
        if any(word in stop_name for word in ["ফতেয়াবাদ", "বটতলী", "ঝাউতলা"]):
            base += 30
        risk_score = round(max(25, min(88, base)), 1)
        
        risk_level = "High" if risk_score > 65 else "Medium" if risk_score > 40 else "Low"
        
        return {
            "stop_name": stop_name,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "peak_hours": "সকাল ৭-৯টা ও বিকেল ৪-৬টায় ঝুঁকি বেশি",
            "note": "⚠️ এই Risk Prediction সম্পূর্ণ সিন্থেটিক ডেটার উপর ভিত্তি করে তৈরি। এটি শুধু সচেতনতার জন্য, বাস্তব তথ্য নয়।"
        }


prediction_service = PredictionService()