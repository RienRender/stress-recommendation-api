from collections import defaultdict
from src.config.supabase_client import supabase



def get_tag_preferences(user_id):

    response = supabase.table("user_activity_interactions") \
        .select("tags, view_time") \
        .eq("user_id", user_id) \
        .execute()

    interactions = response.data

    if not interactions:
        return {}

    tag_scores = defaultdict(float)

    for i in interactions:

        tags = i.get("tags", [])
        weight = i.get("view_time", 1)

        for tag in tags:
            tag_scores[tag] += weight

    total = sum(tag_scores.values())

    if total == 0:
        return {}

    return {
        tag: score / total
        for tag, score in tag_scores.items()
    }