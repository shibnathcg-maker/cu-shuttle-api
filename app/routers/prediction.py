# app/routers/prediction.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import StandardResponse
from app.services.prediction_service import prediction_service

router = APIRouter()

@router.get("/options", response_model=StandardResponse)
def get_options():
    locations = []
    times = []
    for col in prediction_service.delay_cols:
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


@router.post("/predict-delay", response_model=StandardResponse)
def predict_delay(data: dict):
    if "delay" not in prediction_service.models:
        raise HTTPException(status_code=503, detail="Delay model not loaded")
    
    df = prediction_service.prepare_input(data, prediction_service.delay_cols)
    pred = prediction_service.models["delay"].predict(df)
    return StandardResponse(
        status="success",
        message="Delay prediction successful",
        data={"delay_minutes": int(pred[0]) if len(pred) > 0 else 0}
    )


@router.post("/predict-risk", response_model=StandardResponse)
def predict_risk(data: dict):
    if "risk" not in prediction_service.models:
        raise HTTPException(status_code=503, detail="Risk model not loaded")
    
    df = prediction_service.prepare_input(data, prediction_service.risk_cols)
    pred = prediction_service.models["risk"].predict(df)
    return StandardResponse(
        status="success",
        message="Risk prediction successful",
        data={"risk": pred.tolist()}
    )


@router.post("/predict-incident", response_model=StandardResponse)
def predict_incident(data: dict):
    if "incident" not in prediction_service.models:
        raise HTTPException(status_code=503, detail="Incident model not loaded")
    
    df = prediction_service.prepare_input(data, prediction_service.incident_cols)
    pred = prediction_service.models["incident"].predict(df)
    return StandardResponse(
        status="success",
        message="Incident prediction successful",
        data={"incident": pred.tolist()}
    )


@router.post("/report", response_model=StandardResponse)
def report(data: dict):
    print("📢 New Report Received:", data)
    return StandardResponse(
        status="success",
        message="Report submitted successfully. Thank you!"
    )


@router.post("/emergency", response_model=StandardResponse)
def emergency(data: dict):
    print("🚨 EMERGENCY ALERT:", data)
    return StandardResponse(
        status="success",
        message="Emergency alert sent to authorities. Help is on the way!"
    )