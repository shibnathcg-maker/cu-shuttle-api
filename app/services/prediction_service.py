# app/services/prediction_service.py
import joblib
import numpy as np
import os

class PredictionService:
    def __init__(self):
        self.delay_model = None
        self.risk_model = None
        self.load_models()

    def load_models(self):
        try:
            model_dir = "app/ml_models"
            if os.path.exists(f"{model_dir}/delay_model.pkl"):
                self.delay_model = joblib.load(f"{model_dir}/delay_model.pkl")
                print("✅ Delay model loaded")
            else:
                print("⚠️ Delay model not found - using dummy")

            if os.path.exists(f"{model_dir}/risk_model.pkl"):
                self.risk_model = joblib.load(f"{model_dir}/risk_model.pkl")
                print("✅ Risk model loaded")
            else:
                print("⚠️ Risk model not found - using dummy")
        except Exception as e:
            print(f"❌ Model loading failed: {e}")

    def predict_delay(self, train_id: str, hour: int, day_type: str = "weekday"):
        try:
            if self.delay_model is None:
                return self._dummy_delay(train_id, hour)
            
            features = np.array([[float(hour), 1 if day_type.lower() == "weekday" else 0]])
            delay = float(self.delay_model.predict(features)[0])
            delay = max(0, round(delay, 1))
            
            return {
                "train_id": train_id,
                "predicted_delay": delay,
                "status": "Delayed" if delay > 5 else "On Time",
                "note": "⚠️ এই Delay Prediction সিন্থেটিক ডেটা দিয়ে তৈরি। বাস্তব সময়ের সাথে পার্থক্য থাকতে পারে।"
            }
        except:
            return self._dummy_delay(train_id, hour)

    def predict_risk(self, stop_name: str, hour: int, day_type: str = "weekday"):
        try:
            if self.risk_model is None:
                return self._dummy_risk(stop_name, hour)
            
            features = np.array([[float(hour), hash(stop_name) % 20, 1 if day_type.lower() == "weekday" else 0]])
            risk = float(self.risk_model.predict(features)[0])
            risk = max(20, min(90, round(risk, 1)))
            
            level = "High" if risk > 65 else "Medium" if risk > 40 else "Low"
            
            return {
                "stop_name": stop_name,
                "risk_score": risk,
                "risk_level": level,
                "note": "⚠️ এই Risk Prediction সিন্থেটিক ডেটা দিয়ে তৈরি। শুধু সচেতনতার জন্য।"
            }
        except:
            return self._dummy_risk(stop_name, hour)

    def _dummy_delay(self, train_id: str, hour: int):
        delay = round((hour % 9) * 3.5, 1)
        return {
            "train_id": train_id,
            "predicted_delay": delay,
            "status": "Delayed" if delay > 8 else "On Time",
            "note": "⚠️ এই Delay Prediction সিন্থেটিক ডেটা দিয়ে তৈরি। বাস্তব সময়ের সাথে পার্থক্য থাকতে পারে।"
        }

    def _dummy_risk(self, stop_name: str, hour: int):
        base = 45 + (hour % 12) * 4
        if any(x in stop_name for x in ["ফতেয়াবাদ", "বটতলী", "ঝাউতলা"]):
            base += 25
        risk = round(max(25, min(85, base)), 1)
        level = "High" if risk > 65 else "Medium" if risk > 40 else "Low"
        return {
            "stop_name": stop_name,
            "risk_score": risk,
            "risk_level": level,
            "note": "⚠️ এই Risk Prediction সিন্থেটিক ডেটা দিয়ে তৈরি। শুধু সচেতনতার জন্য।"
        }


prediction_service = PredictionService()
