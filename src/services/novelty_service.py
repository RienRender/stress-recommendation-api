from collections import defaultdict
from src.config.supabase_client import supabase


def get_activity_counts(user_id):

    response = supabase.table("user_activity_interactions") \
        .select("activity_id") \
        .eq("user_id", user_id) \
        .execute()

    interactions = response.data

    counts = defaultdict(int)

    for i in interactions:
        counts[i["activity_id"]] += 1

    return counts


def novelty_bonus(user_id, activity_id):

    counts = get_activity_counts(user_id)

    # number of times user has seen this activity
    n = counts.get(activity_id, 0)

    # novelty formula
    bonus = 1 / (1 + n)

    return bonus * 1.0   # scale (tunable)

def novelty_from_counts(activity_counts, activity_id):

    n = activity_counts.get(activity_id, 0)

    bonus = 1 / (1 + n)

    return bonus * 0.3