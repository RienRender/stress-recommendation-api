from src.config.supabase_client import supabase

def load_activities():
    response = supabase.table("activities").select("*").execute()

    if response.data is None:
        return []

    return response.data