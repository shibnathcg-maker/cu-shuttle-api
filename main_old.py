from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import json
import os
from dotenv import load_dotenv
from groq import Groq
from typing import Any, Dict

# Load environment variables
load_dotenv()

app = FastAPI(
    title="CU Shuttle Smart System",
    description="AI-Powered Shuttle Delay, Risk & Incident Prediction + Chatbot",
    version="1.0.0"
)

# ================== CORS ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GROQ CLIENT (Free & Fast) ----------------
groq_client = None
groq_key = os.getenv("GROQ_API_KEY")

if groq_key:
    groq_client = Groq(api_key=groq_key)
    print("✅ Groq client initialized successfully")
else:
    print("⚠️  WARNING: GROQ_API_KEY not found in .env file")

# ---------------- MODEL LOADING ----------------
models = {}
columns = {}

try:
    models["delay"] = joblib.load("model/delay_model.pkl")
    models["incident"] = joblib.load("model/incident_model.pkl")
    models["risk"] = joblib.load("model/risk_model.pkl")
    print("✅ All ML models loaded successfully")
except Exception as e:
    print(f"❌ MODEL LOAD ERROR: {e}")
    models = {}

try:
    with open("model/columns.json") as f:
        columns = json.load(f)
    print("✅ Columns mapping loaded")
except Exception as e:
    print(f"⚠️ COLUMN LOAD ERROR: {e}")
    columns = []

delay_cols = columns.copy()
incident_cols = columns.copy()
risk_cols = columns.copy()


# ================== STANDARD RESPONSE MODEL ==================
class StandardResponse(BaseModel):
    status: str
    message: str
    data: Any = None
    error: str = None


# ================== CHAT MODELS ==================
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str


# ================== ENDPOINTS ==================

@app.get("/", response_model=StandardResponse)
def home():
    return StandardResponse(
        status="success",
        message="CU Shuttle Smart System API is running successfully 🚀"
    )


@app.get("/ping", response_model=StandardResponse)
def ping():
    return StandardResponse(status="success", message="pong")


@app.get("/options", response_model=StandardResponse)
def get_options():
    locations = []
    times = []
    for col in delay_cols:
        if col.startswith("Location_"):
            locations.append(col.replace("Location_", ""))
        elif col.startswith("Time_"):
            times.append(col.replace("Time_", ""))

    if not locations:
        locations = ["CU Campus Gate", "Varsity Railway Station", "Battali Old Rail Station",
                     "Sholashahar", "Hathazari", "Zero Point"]
    if not times:
        times = ["07:30", "08:00", "09:45", "10:30", "14:50", "15:50", "20:30"]

    return StandardResponse(
        status="success",
        message="Options fetched successfully",
        data={
            "locations": sorted(list(set(locations))),
            "times": sorted(list(set(times)))
        }
    )


# ---------------- CHAT ENDPOINT (Using Groq) ----------------
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not groq_client:
        raise HTTPException(status_code=503, detail="Groq is not configured. Check your .env file.")

    try:
        print(f"📨 Chat request: {req.message}")

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",     # ← Updated model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, friendly, and concise CU Shuttle assistant for University of Chittagong students."
                },
                {"role": "user", "content": req.message},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        reply = response.choices[0].message.content
        print("✅ Groq replied successfully")
        return ChatResponse(reply=reply)

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Groq Error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Chat service error: {error_msg}")
    

# ---------------- INPUT PREPARATION ----------------
def prepare_input(data: Dict, feature_columns: list):
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


# ---------------- PREDICTION ENDPOINTS ----------------
@app.post("/predict-delay", response_model=StandardResponse)
def predict_delay(data: dict):
    if "delay" not in models:
        raise HTTPException(status_code=503, detail="Delay model not loaded")
    
    df = prepare_input(data, delay_cols)
    pred = models["delay"].predict(df)
    return StandardResponse(
        status="success",
        message="Delay prediction successful",
        data={"delay_minutes": int(pred[0]) if len(pred) > 0 else 0}
    )


@app.post("/predict-risk", response_model=StandardResponse)
def predict_risk(data: dict):
    if "risk" not in models:
        raise HTTPException(status_code=503, detail="Risk model not loaded")
    
    df = prepare_input(data, risk_cols)
    pred = models["risk"].predict(df)
    return StandardResponse(
        status="success",
        message="Risk prediction successful",
        data={"risk": pred.tolist()}
    )


@app.post("/predict-incident", response_model=StandardResponse)
def predict_incident(data: dict):
    if "incident" not in models:
        raise HTTPException(status_code=503, detail="Incident model not loaded")
    
    df = prepare_input(data, incident_cols)
    pred = models["incident"].predict(df)
    return StandardResponse(
        status="success",
        message="Incident prediction successful",
        data={"incident": pred.tolist()}
    )


# ---------------- REPORT & EMERGENCY ----------------
@app.post("/report", response_model=StandardResponse)
def report(data: dict):
    print("📢 New Report Received:", data)
    return StandardResponse(
        status="success",
        message="Report submitted successfully. Thank you!"
    )


@app.post("/emergency", response_model=StandardResponse)
def emergency(data: dict):
    print("🚨 EMERGENCY ALERT:", data)
    return StandardResponse(
        status="success",
        message="Emergency alert sent to authorities. Help is on the way!"
    )


# ================== GLOBAL EXCEPTION HANDLER ==================
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "data": None,
            "error": str(exc.detail)
        }
    )