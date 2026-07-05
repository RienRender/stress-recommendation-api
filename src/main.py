from fastapi import FastAPI
from src.api.routes.recommend import router as recommend_router
from src.services.activity_service import ActivityService


# ✅ CREATE APP FIRST (THIS IS WHAT YOU'RE MISSING)
app = FastAPI()

# ✅ IMPORT ROUTES AFTER
from src.api.activity_routes import router as activity_router
from src.api.activity_create_routes import router as create_router

# ✅ REGISTER ROUTES
app.include_router(activity_router)
app.include_router(create_router)
app.include_router(recommend_router)
ActivityService()
