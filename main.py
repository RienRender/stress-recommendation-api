import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.activity_routes import router as activity_router

app = FastAPI(title="Unified Bandit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")

def read_root():
    return {"status": "AI Brain Active", "version": "Contextual Bandit 21-Feature"}

app.include_router(activity_router)