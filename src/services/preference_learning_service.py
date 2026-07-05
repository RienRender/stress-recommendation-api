from collections import defaultdict
from src.config.supabase_client import supabase


CATEGORY_MAP = {
    "breathing": "mindfulness",
    "meditation": "mindfulness",
    "relax": "mindfulness",

    "exercise": "physical",
    "walk": "physical",
    "stretch": "physical",

    "drawing": "creative",
    "music": "creative",
    "writing": "creative",

    "video": "entertainment",
    "game": "entertainment"
}


def get_user_preferences(user_id):

    response = supabase.table("user_activity_interactions") \
        .select("tags, view_time") \
        .eq("user_id", user_id) \
        .execute()

    interactions = response.data

    if not interactions:
        return {
            "mindfulness": 0.5,
            "physical": 0.5,
            "creative": 0.5,
            "entertainment": 0.5
        }

    scores = defaultdict(float)

    for i in interactions:

        tags = i.get("tags", [])
        weight = i.get("view_time", 1)

        for tag in tags:

            category = CATEGORY_MAP.get(tag)

            if category:
                scores[category] += weight

    total = sum(scores.values())

    if total == 0:
        return {
            "mindfulness": 0.5,
            "physical": 0.5,
            "creative": 0.5,
            "entertainment": 0.5
        }

    return {
        "mindfulness": scores["mindfulness"] / total,
        "physical": scores["physical"] / total,
        "creative": scores["creative"] / total,
        "entertainment": scores["entertainment"] / total
    }