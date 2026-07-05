import os
import random
import pickle
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional

# Service Imports
from src.recommendation.recommendation_service import RecommendationService, reward_history
from src.models.request_models import RecommendRequest, FeedbackRequest
from src.config.supabase_client import supabase

router = APIRouter()

# --- 1. Response Models ---

class ActivityItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    instructions: Optional[str] = ""
    emoji: str = "🌸"
    activity_type: str = "general"
    duration: str = "15"
    location: Optional[str] = "Remote"
    max_participants: int = 10
    enrolled_count: int = 1
    host_name: str = "System"
    indoor_outdoor: int = 0
    energy_required: int = 0
    privacy: int = 0
    tags: List[str] = []
    start_date: str = ""
    completed_at: Optional[str] = None
    is_canceled: bool = False
    match_score: float
    arm: int
    is_preset: bool = False



class RecommendationResponse(BaseModel):
    recommended: List[ActivityItem]
    good_options: List[ActivityItem]
    something_new: List[ActivityItem]


# --- 2. Routes ---

@router.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendRequest):
    """🚀 Triggers Step 1, 2, 3, 4 logs in terminal"""
    try:
        service = RecommendationService(user_id=request.user_id)
        result = service.recommend_activity(request)
        return result
    except Exception as e:
        print(f"🚨 RECOMMEND ROUTE ERROR: {e}")
        return {"recommended": [], "good_options": [], "something_new": []}


@router.post("/feedback")
def feedback(data: FeedbackRequest):
    # 🕵️ HEARTBEAT
    print(f"\n🔔 REQUEST RECEIVED: Feedback for user {data.user_id}")
    print(f"📦 Payload: Activity={data.activity_id}, Arm={data.arm}, Context Length={len(data.context)}")

    try:
        service = RecommendationService(user_id=data.user_id)

        # 🚀 This triggers the 6️⃣ and 7️⃣ logs
        reward = service.process_feedback_and_learn(data.dict())

        reward_history.append(reward)
        return {"status": "success", "reward": reward, "message": "AI Brain updated and logs printed to terminal. 🧠"}
    except Exception as e:
        print(f"🚨 ROUTE ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/debug-feedback")
async def debug_feedback(request: Request):
    body = await request.json()
    print("\n🚨 DEBUG: RAW DATA RECEIVED!")
    print(body)
    return {"status": "received"}


# --- 3. Dashboard & Visualization ---

@router.get("/dashboard")
def dashboard(user_id: str = "default_user_id"):
    """
    Exposes the deep Contextual Bandit matrix to the UI Dashboard.
    Pass a specific user_id as a query param to see their exact brain.
    """
    import numpy as np
    from src.recommendation.recommendation_service import reward_history, latest_ranking
    from src.bandit.model_registry import get_model

    # 1. Fetch the user's specific ML brain
    bandit = get_model(user_id)

    # 2. Calculate the raw Theta (Learned Weights)
    A_inv = np.linalg.inv(bandit.A)
    theta = A_inv @ bandit.b

    # 3. Define the 21 Feature Names (Must match the Python exact list)
    feature_names = [
        "stress_norm", "mindful_pref", "phys_pref", "creative_pref", "entert_pref",
        "social_pref", "energy_level", "time_cat_norm", "happy_norm", "loc_pref",
        "tag_similarity", "tag_match_ratio", "novelty_bonus", "rep_penalty",
        "is_mindful", "is_physical", "is_creative", "is_entert", "dur_norm", "pop_score", "loc_numeric"
    ]

    # 4. We simulate the latest 'x' input if there is a recent ranking,
    # otherwise we just show the weights (theta).
    current_context = []

    # Note: In a real production app, you'd save the last 'x' vector to memory
    # to display it accurately here. For now, we will show the Theta weights.
    for idx, name in enumerate(feature_names):
        weight = float(theta[idx])
        current_context.append({
            "dim": idx + 1,
            "name": name,
            "x": 1.0,  # Placeholder for live 'x'. You can pipe this from recommendation_service!
            "theta": weight
        })

    return {
        "rewards": [float(r) for r in reward_history],
        "avg_reward": sum(reward_history) / len(reward_history) if reward_history else 0,
        "latest_ranking": [
            {"activity": str(item.get("activity", {}).get("title", "Unknown")), "score": float(item.get("score", 0))}
            for item in latest_ranking
        ],
        "current_context": current_context
    }

@router.get("/plot-scores")
def plot_scores():
    from src.recommendation.recommendation_service import score_history
    plt.figure()
    for name, history in score_history.items():
        plt.plot(history, label=name)

    plt.legend()
    plt.title("Activity Score Learning Over Time")
    plt.xlabel("Steps")
    plt.ylabel("Score")
    plt.savefig("score_learning.png")
    plt.close()
    return {"status": "saved as score_learning.png"}