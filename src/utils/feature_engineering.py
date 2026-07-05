import numpy as np

def build_context_vector(user_state, user_prefs, activity, stats):
    # 1. User Features (10)
    stress_score_norm = float(user_state.get("stress_score") or 50) / 100.0
    energy_level = float(user_state.get("energy_level") or 0.5)
    available_time_norm = float(user_state.get("available_time_category") or 3) / 5.0
    happiness_norm = float(user_state.get('happiness', 5.5)) / 10.0
    location_pref = float(user_state.get("location_preference") or 0)
    social_pref = float(user_state.get("social_preference") or 0)

    # These come from build_user_preferences
    mindfulness_pref = float(user_prefs.get("mindfulness") or 0.5)
    physical_pref = float(user_prefs.get("physical") or 0.5)
    creative_pref = float(user_prefs.get("creative") or 0.5)
    entertainment_pref = float(user_prefs.get("entertainment") or 0.5)

    # 2. Activity Features (11)
    tag_similarity = float(stats.get("tag_similarity") or 0.0)
    tag_match_ratio = float(stats.get("tag_match_ratio") or 0.0)
    novelty_bonus = float(stats.get("novelty") or 0.0)
    repetition_penalty = float(stats.get("repetition_penalty") or 0.0)

    a_type = activity.get("activity_type") or "general"
    is_m = 1.0 if a_type == "mindfulness" else 0.0
    is_p = 1.0 if a_type == "physical" else 0.0
    is_c = 1.0 if a_type == "creative" else 0.0
    is_e = 1.0 if a_type == "entertainment" else 0.0

    duration_val = float(activity.get("duration") or 15)
    duration_norm = duration_val / 60.0

    # 🚀 DIMENSION 20: GLOBAL POPULARITY (Using the enrolled count)
    # We normalize it by 20. If 20 people have done it, it gets a max score of 1.0!
    act_enrolled = int(activity.get('enrolled', 0))
    popularity = min(act_enrolled / 20.0, 1.0)

    # 3. Location Mapping
    loc_map = {"Quiet Space": 0.0, "Indoor": 1.0, "Outdoor": 2.0, "Remote": 3.0, "Gym": 4.0}
    loc_numeric = loc_map.get(activity.get('location'), 1.0)

    return [
        stress_score_norm, mindfulness_pref, physical_pref, creative_pref,
        entertainment_pref, social_pref, energy_level, available_time_norm,
        happiness_norm, location_pref,
        tag_similarity, tag_match_ratio, novelty_bonus, repetition_penalty,
        is_m, is_p, is_c, is_e, duration_norm, popularity, loc_numeric
    ]


def build_user_preferences(user_profile):
    """REAL DATA: Onboarding Strings -> Math Floats"""
    energy_map = {"Low Energy": 0.2, "Medium": 0.5, "High Energy": 0.9}
    social_map = {"Mostly Alone": 0.1, "Small Groups": 0.5, "Large Groups": 0.9}

    enjoyed = user_profile.get("pref_activities") or []

    return {
        "mindfulness": 1.0 if any(x in enjoyed for x in ['Meditation', 'Breathing']) else 0.5,
        "physical": 1.0 if any(x in enjoyed for x in ['Exercise', 'Running', 'Yoga']) else 0.5,
        "creative": 1.0 if any(x in enjoyed for x in ['Drawing', 'Writing']) else 0.5,
        "entertainment": 1.0 if any(x in enjoyed for x in ['Music', 'Videos']) else 0.5,
        "energy": energy_map.get(user_profile.get("pref_energy"), 0.5),
        "social": social_map.get(user_profile.get("pref_social"), 0.5)
    }


# Ensure these helpers are present for the service to call
def compute_tag_similarity(u_tags, a_tags):
    u, a = set(u_tags), set(a_tags)
    return len(u & a) / len(u | a) if len(u | a) > 0 else 0.0


def build_activity_stats(user_tags, activity, history, global_stats):
    aid = str(activity.get("id", ""))
    a_tags = activity.get("tags", [])
    seen = history.get("times_seen", {}).get(aid, 0)
    recent = history.get("times_recent", {}).get(aid, 0)

    return {
        "tag_similarity": compute_tag_similarity(user_tags, a_tags),
        "tag_match_ratio": len(set(user_tags) & set(a_tags)) / len(a_tags) if a_tags else 0.0,
        "novelty": 1.0 / (1.0 + seen),
        "repetition_penalty": min(recent / 5.0, 1.0)
        # Note: popularity is now handled directly in build_context_vector via the enrolled count!
    }