from src.config.supabase_client import supabase


def get_user_preferences(user_id):

    response = supabase.table("user_activity_interactions") \
        .select("activity_id, view_time") \
        .eq("user_id", user_id) \
        .execute()

    interactions = response.data

    if not interactions:
        return {
            "mindfulness": 0.25,
            "physical": 0.25,
            "creative": 0.25,
            "entertainment": 0.25
        }

    type_counts = {
        "mindfulness": 0,
        "physical": 0,
        "creative": 0,
        "entertainment": 0
    }

    for interaction in interactions:

        activity = supabase.table("activities") \
            .select("activity_type") \
            .eq("id", interaction["activity_id"]) \
            .single() \
            .execute()

        activity_type = activity.data["activity_type"]

        weight = interaction.get("view_time", 1)

        type_counts[activity_type] += weight

    total = sum(type_counts.values())

    return {
        k: v / total for k, v in type_counts.items()
    }