from src.config.supabase_client import supabase

def save_interaction(data, reward):
    supabase.table("user_activity_interactions").insert({
        "user_id": data.user_id,
        "activity_id": data.activity_id,
        "stress_before": data.stress_before,
        "stress_after": data.stress_after,
        "rating": data.rating,
        "happiness": data.happiness,  # ✅ NEW
        "view_time": data.view_time,
        "completed": data.completed,
        "reward": reward
    }).execute()