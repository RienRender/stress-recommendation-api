from fastapi import APIRouter
from src.config.supabase_client import supabase
from src.services.tag_service import register_tags, bootstrap_user_tags
from src.models.activity_models import CreateActivityRequest

router = APIRouter()

@router.post("/create-activity")
def create_activity(data: CreateActivityRequest):

    payload = data.dict()

    response = supabase.table("activities").insert(payload).execute()
    activity = response.data[0]

    register_tags(payload.get("tags", []))
    bootstrap_user_tags(payload["user_id"], payload.get("tags", []))

    return {
        "status": "created",
        "activity": activity
    }