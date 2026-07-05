from fastapi import APIRouter, HTTPException, Query
from src.recommendation.recommendation_service import RecommendationService
from src.config.supabase_client import supabase
from pydantic import BaseModel

class RecommendRequest(BaseModel):
    user_id: int
    stress_score: float
    energy_level: float
    available_time_category: int   # ✅ UPDATED
    social_preference: float = 0
    happiness: float = 0.5
    location_preference: int = 0   # ✅ NEW
    
router = APIRouter()
service = None


@router.post("/recommend")
def recommend_activity_route(data: RecommendRequest):
    global service

    if service is None:
        service = RecommendationService()

    try:
        result = service.recommend_activity(data.dict())

        activity = result["activity"]
        scores = result["scores"]

        return {
            "activity": {
                "id": activity.get("id"),
                "name": activity.get("title"),
                "description": activity.get("description"),
                "tags": activity.get("tags", [])
            },
            "scores": scores
        }

    except Exception as e:
        print("RECOMMEND ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


# 🔥 FIXED TAG SUGGESTION ROUTE
@router.get("/tags/suggest")
def suggest_tags(query: str = Query(...)):
    try:
        res = supabase.table("tags") \
            .select("tag_name") \
            .ilike("tag_name", f"{query}%") \
            .limit(5) \
            .execute()

        return [row["tag_name"] for row in res.data]

    except Exception as e:
        print("TAG SUGGEST ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))