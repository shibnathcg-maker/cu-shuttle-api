# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import StandardResponse
from app.routers.chat import router as chat_router
from app.routers.prediction import router as prediction_router

app = FastAPI(
    title="CU Shuttle Smart System",
    description="AI-Powered Shuttle System for University of Chittagong",
    version="1.0.0"
)

# CORS - Very Important for Lovable Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers — NO prefix so URLs work correctly
app.include_router(chat_router)
app.include_router(prediction_router)

# Basic Routes
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
    locations = [
        "CU Campus", "Jhautala", "Sholashahar", "Fatehbad",
        "Chowdhuri Haat", "Ctg Polytechnic", "Ctg Cantonment", "Bottoli"
    ]
    times = [
        "07:15 AM", "07:40 AM", "08:40 AM", "09:05 AM", "10:30 AM",
        "01:00 PM", "02:00 PM", "02:30 PM", "03:35 PM", "04:40 PM",
        "05:00 PM", "06:20 PM"
    ]
    routes = ["Bottoli-CU", "CU-Bottoli"]

    return StandardResponse(
        status="success",
        message="Options fetched successfully",
        data={
            "locations": locations,
            "times": times,
            "routes": routes
        }
    )