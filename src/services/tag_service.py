from src.config.supabase_client import supabase
from supabase import create_client  # or your existing import

# ------------------------
# REGISTER TAGS
# ------------------------
def register_tags(tags):

    for tag in tags:
        supabase.table("tags").upsert({
            "tag": tag
        }).execute()


# ------------------------
# BOOTSTRAP USER TAGS
# ------------------------
def bootstrap_user_tags(user_id, tags):

    for tag in tags:
        supabase.table("user_tag_stats").upsert({
            "user_id": user_id,
            "tag": tag,
            "score": 0.3
        }).execute()


# ------------------------
# TAG SIMILARITY (INTELLIGENT)
# ------------------------
def tag_similarity(tag1, tag2):

    tag1 = tag1.lower()
    tag2 = tag2.lower()

    # simple semantic rules (expandable)
    similar_groups = [
        ["yoga", "stretching", "flexibility"],
        ["run", "jog", "walking"],
        ["music", "song", "instrument"],
        ["meditation", "mindfulness", "breathing"]
    ]

    if tag1 == tag2:
        return 1.0

    for group in similar_groups:
        if tag1 in group and tag2 in group:
            return 0.7

    return 0.0


# ------------------------
# SMART TAG MATCH
# ------------------------
def compute_tag_match(user_tags, activity_tags):

    if isinstance(activity_tags, str):
        activity_tags = activity_tags.split(",")

    if not activity_tags:
        return 0

    score = 0

    for a_tag in activity_tags:
        best = 0
        for u_tag in user_tags:
            sim = tag_similarity(a_tag, u_tag)
            best = max(best, sim)
        score += best

    return score / len(activity_tags)



def normalize_tag(tag: str):
    return tag.strip().lower()


def get_or_create_tag(tag_name: str, activity_type: str, source="global", user_id=None):
    tag_name = normalize_tag(tag_name)

    existing = supabase.table("tags") \
        .select("tag_id") \
        .eq("tag_name", tag_name) \
        .eq("activity_type", activity_type) \
        .execute()

    if existing.data:
        return existing.data[0]["tag_id"]

    new_tag = supabase.table("tags").insert({
        "tag_name": tag_name,
        "activity_type": activity_type,
        "source": source,
        "created_by": user_id
    }).execute()

    return new_tag.data[0]["tag_id"]


def attach_tags_to_activity(activity_id: int, tag_ids: list):
    for tag_id in tag_ids:
        supabase.table("activity_tags").insert({
            "activity_id": activity_id,
            "tag_id": tag_id
        }).execute()


def get_activity_tags(activity_id: int):
    res = supabase.table("activity_tags") \
        .select("tag_id") \
        .eq("activity_id", activity_id) \
        .execute()

    return [t["tag_id"] for t in res.data]