from fastapi import APIRouter
from src.logging.replay_logger import ReplayLogger

router = APIRouter()
logger = ReplayLogger()


@router.post("/feedback")
def log_feedback(data: dict):

    logger.log({
        "user_id": data["user_id"],
        "stress_level": data["stress_level"],
        "activity": data["activity"],
        "reward": data["reward"],
        "view_time": data["view_time"],
        "view_count": data["view_count"],
        "novelty_bonus": data["novelty_bonus"],
        "interest_score": data["interest_score"]
    })

    return {"status": "logged"}