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

# Include Routers
app.include_router(chat_router)
app.include_router(prediction_router, prefix="/api")

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