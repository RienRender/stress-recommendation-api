def log_interaction(data):

    supabase.table("user_activity_interactions").insert(data).execute()