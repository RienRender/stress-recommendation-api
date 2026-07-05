from src.config.supabase_client import supabase


def get_tag_vocabulary(user_id):
    """
    Returns 30 tags:
    10 global + 10 personal + 10 community
    """

    # 1. Global tags
    global_tags = supabase.table("tags") \
        .select("tag_name") \
        .eq("tag_source", "global") \
        .limit(10) \
        .execute().data

    # 2. Personal tags
    personal_tags = supabase.table("user_tag_stats") \
        .select("tag_name") \
        .eq("user_id", user_id) \
        .order("usage_count", desc=True) \
        .limit(10) \
        .execute().data

    # 3. Community tags
    community_tags = supabase.table("tag_usage_stats") \
        .select("tag_name") \
        .order("usage_count", desc=True) \
        .limit(10) \
        .execute().data

    vocab = (
        [t["tag_name"] for t in global_tags] +
        [t["tag_name"] for t in personal_tags] +
        [t["tag_name"] for t in community_tags]
    )

    return list(dict.fromkeys(vocab))[:30]  # remove duplicates


def activity_to_vector(activity_id, vocab):
    """
    Convert activity → 30-dim vector
    """

    # get activity tags
    res = supabase.table("activity_tags") \
        .select("tags(tag_name)") \
        .eq("activity_id", activity_id) \
        .execute()

    activity_tags = [t["tags"]["tag_name"] for t in res.data]

    # build vector
    vector = [1 if tag in activity_tags else 0 for tag in vocab]

    return vector