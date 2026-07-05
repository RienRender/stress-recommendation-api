from src.config.supabase_client import supabase


class ActivityService:

    def get_all(self):
        res = supabase.table("activities").select("*").execute()
        return res.data