import random
import numpy as np
from datetime import datetime, timedelta, timezone
from src.config.supabase_client import supabase
from src.utils.feature_engineering import (
    build_context_vector,
    build_activity_stats,
    build_user_preferences
)
from src.bandit.model_registry import get_model

# Global Tracking
reward_history = []
score_history = {}
latest_ranking = []


class RecommendationService:
    def __init__(self, user_id: str):
        self.user_id = str(user_id)
        self.bandit = get_model(self.user_id)

    def _load_activities_from_db(self):
        try:
            res = supabase.table("activities").select("*").execute()
            return res.data if res and hasattr(res, 'data') else []
        except:
            return []

    def recommend_activity(self, user_state):
        if hasattr(user_state, "dict"): user_state = user_state.dict()
        user_id = user_state.get("user_id", self.user_id)

        print("\n" + "═" * 115)
        print(
            f" 1️⃣  USER INPUT STATE: Stress={user_state.get('stress_score')} | Happy={user_state.get('happiness')} | Time={user_state.get('available_time_category')}")

        # 1. Get the perfectly tagged pool sent from Flutter
        candidates = user_state.get("activity_pool", [])

        # --- PHASE 1: THE HARD FILTERS ---
        ov_energy = user_state.get("energy_override")
        ov_social = user_state.get("social_override")  # 0=Alone, 1=Friends
        ov_loc = user_state.get("location_override")  # 0=Indoor, 1=Outdoor, 2=Both

        print(f"\n🎯 DEBUG -> FLUTTER SENT: Energy={ov_energy}, Social={ov_social}, Loc={ov_loc}")

        now = datetime.now(timezone.utc)  # Get current time in UTC
        filtered_candidates = []

        for act in candidates:

            is_friend = act.get('is_friend_flag', 0) == 1
            # 🛡️ HARD SECURITY LOCK
            act_privacy = int(act.get('privacy', 0))
            is_me = str(act.get('host_id')) == str(user_id)

            # Only skip privacy 0 if it's a HUMAN activity that isn't yours.
            # System presets (host_id is None) must always pass this check.
            if act_privacy == 0 and act.get('host_id') is not None and not is_me:
                continue

            # Existing social and owner filters
            is_friend = act.get('is_friend_flag', 0) == 1
            if act_privacy == 1 and not is_friend and not is_me:
                continue

                # --- KEEP ALL OTHER TEMPORAL/LIVE FILTERS BELOW ---
            # Change this line in your loop:
            is_preset = act.get('host_id') is None or act.get('host_name') == 'System' or act.get('is_system_flag') == 1
            is_fav = act.get('is_favorite_flag', 0) == 1

            # Parse the start date from the activity
            start_str = act.get('start_date')
            try:
                start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            except:
                start_dt = now  # Fallback if date is missing

            # 🛑 STRICT RULE: Human activities expire. Presets and Favorites do NOT.
            is_preset = (
                    act.get('host_id') is None or
                    act.get('host_name') == 'System' or
                    act.get('is_system_flag', 0) == 1 or
                    act.get('is_preset', False) is True
            )

            if not is_fav and not is_preset:
                if now >= start_dt:
                    print(f"Skipping expired human activity: {act.get('title')}")
                    continue

            is_friend = act.get('is_friend_flag', 0) == 1
            act_loc = int(act.get('indoor_outdoor', 2))
            act_energy = int(act.get('energy_required', 1))
            act_privacy = int(act.get('privacy', 0))

            keep = True

            # 🛑 Location Filter
            if ov_loc not in [None, ""] and int(ov_loc) != 2 and act_loc != 2:
                if act_loc != int(ov_loc):
                    keep = False

            # 🛑 Energy Filter
            if ov_energy not in [None, ""]:
                if act_energy != int(ov_energy):
                    keep = False

            # 🛑 Social Filter
            if not is_friend and ov_social not in [None, ""]:
                wants_alone = int(ov_social) == 0
                is_group_activity = act_privacy > 0

                if wants_alone and is_group_activity:
                    keep = False  # Wants alone, reject group presets
                elif not wants_alone and not is_group_activity:
                    keep = False  # Wants friends, reject solo presets

            if keep:
                filtered_candidates.append(act)

        # 🛡️ THE FALLBACK SAFETY NET
        if not filtered_candidates:
            print("\n🚨 WARNING: 0 MATCHES FOUND! The user's strict filters eliminated every activity.")
            print(f"Filters used -> Energy: {ov_energy}, Social: {ov_social}, Location: {ov_loc}")
            print("Falling back to standard recommendations to prevent a crash.\n")
            filtered_candidates = [a for a in candidates if a.get('is_system_flag', 0) == 1]

        if not filtered_candidates:
            return {"recommended": [], "good_options": [], "something_new": []}

        # Build prerequisites for Context Vector
        profile = self._get_user_profile(user_id)
        user_prefs = build_user_preferences(profile)
        history = self._get_user_history(user_id)
        global_stats = self._get_global_stats()

        sample_act = filtered_candidates[0]
        print(f"\n 2️⃣  21-DIMENSIONAL CONTEXT TRACE (Target: {sample_act.get('title', 'Untitled')})")
        print(f"{'DIM':<4} | {'FEATURE NAME':<22} | {'EXACT CALCULATION':<35} | {'RESULT'}")
        print("-" * 115)
        act_stats = build_activity_stats(profile.get('pref_activities', []), sample_act, history, global_stats)
        x_trace = build_context_vector(user_state, user_prefs, sample_act, act_stats)
        self._print_full_21d_trace(x_trace, sample_act, user_state, profile, history, global_stats)

        # --- PHASE 2: LINUCB SCORING ---
        scored_items = []
        print(f"\n 3️⃣  LINUCB SCORING: Score = (θ · x) + (α * √(xᵀ A⁻¹ x))")
        print(f"{'ACTIVITY TITLE':<30} | {'EXPLOIT (θ · x)':<18} | {'EXPLORE (α * √)':<25} | {'TOTAL'}")
        print("-" * 115)

        A_inv = np.linalg.inv(self.bandit.A)
        theta = A_inv @ self.bandit.b
        alpha = self.bandit.alpha

        for act in filtered_candidates:
            act_stats = build_activity_stats(profile.get('pref_activities', []), act, history, global_stats)
            x = np.array(build_context_vector(user_state, user_prefs, act, act_stats)).flatten()

            # 🧮 The Core Math
            exploit = float(np.dot(theta, x))
            uncertainty = float(np.sqrt(x.dot(A_inv).dot(x)))
            explore = alpha * uncertainty

            # Boost favorites slightly in the exploit score
            is_fav = act.get('is_favorite_flag', 0) == 1
            if is_fav: exploit += 0.30

            total = exploit + explore

            # 🚀 THE TRACE PRINT YOU WANTED:
            title_display = act.get('title', 'Untitled')[:30]
            print(f"{title_display:<30} | {exploit:18.4f} | {alpha} * {uncertainty:.4f} | {total:8.4f}")

            scored_items.append({
                "activity": act,
                "score": total,
                "explore_score": explore,
                "is_friend": act.get('is_friend_flag', 0) == 1,
                "is_fav": is_fav,
                "arm": 0
            })

            # --- PHASE 3: NORMALIZATION & BUCKETING ---
        if scored_items:
            scored_items.sort(key=lambda x: x["score"], reverse=True)
            max_s, min_s = scored_items[0]["score"], scored_items[-1]["score"]
            s_range = max_s - min_s if max_s > min_s else 1.0
            for item in scored_items:
                norm = (item["score"] - min_s) / s_range
                item["human_match_score"] = 0.75 + (norm * 0.23)

        # --- PHASE 3: THE UI BUCKETING & REASONING ---
        recommended = []
        good_options = []
        something_new = []

        # We work on a copy to avoid index errors while removing
        pool = list(scored_items)

        # 1. Grab Social/Friends first for "Something New" (Limit 2)
        for x in pool[:]:
            if x['is_friend'] and len(something_new) < 2:
                x['reason'] = "Social Connection (Friend Activity)"
                something_new.append(x)
                pool.remove(x)

        # 2. Grab Favorites for "Good Options" (Limit 2)
        for x in pool[:]:
            if x['is_fav'] and len(good_options) < 2:
                x['reason'] = "User Preference (Saved Favorite)"
                good_options.append(x)
                pool.remove(x)

        # 3. Fill "Recommended" with top scores
        wants_alone = (ov_social == 0) or (ov_social == "0")
        for x in pool[:]:
            if len(recommended) < 2:
                if wants_alone and x['is_friend']: continue

                # 🚀 THE LOGIC FIX: Check if we actually have Exploit data
                if x['score'] - x['explore_score'] > 0.1:  # If Exploit is significant
                    x['reason'] = "High AI Confidence (Learned Preference)"
                else:
                    x['reason'] = "Cold Start: High Exploration Priority"

                recommended.append(x)
                pool.remove(x)

            # 4. Fill "Good Options"
        for x in pool[:]:
            if len(good_options) < 3:
                if x['score'] - x['explore_score'] > 0.1:
                    x['reason'] = "Solid Match (Historical Success)"
                else:
                    x['reason'] = "Contextual Match (First-time Trial)"

                good_options.append(x)
                pool.remove(x)

        # 5. Fill remaining "Something New" with high uncertainty (Explore score)
        pool.sort(key=lambda x: x['explore_score'], reverse=True)
        for x in pool[:]:
            if len(something_new) < 3:
                x['reason'] = "AI Discovery (High Uncertainty)"
                something_new.append(x)
                pool.remove(x)

        # 📊 PRINT TOP 5 SUMMARY (SAFE ACCESS)
        print(f"\n 📊 FINAL AI RANKING (Top 5)")
        print(f"{'ACTIVITY TITLE':<30} | {'RAW UCB SCORE':<15} | {'UX MATCH %':<10}")
        print("-" * 65)
        all_final = recommended + good_options + something_new
        for item in all_final[:5]:
            title = item['activity'].get('title', 'Untitled')[:30]
            score = item.get('score', 0.0)
            ux = item.get('human_match_score', 0.85) * 100
            print(f"{title:<30} | {score:15.4f} | {ux:.0f}%")

        # 🧠 PRINT BUCKET LOGIC TRACE (THE "WHY")
        print(f"\n 🧠 BUCKET LOGIC TRACE: Why were these chosen?")
        print(f"{'CATEGORY':<15} | {'ACTIVITY':<25} | {'LOGIC REASON'}")
        print("-" * 85)
        for x in recommended:
            print(f"{'RECOMMENDED':<15} | {x['activity'].get('title')[:25]:<25} | {x.get('reason')}")
        for x in good_options:
            print(f"{'GOOD OPTIONS':<15} | {x['activity'].get('title')[:25]:<25} | {x.get('reason')}")
        for x in something_new:
            print(f"{'SOMETHING NEW':<15} | {x['activity'].get('title')[:25]:<25} | {x.get('reason')}")

        print("\n" + "═" * 115 + "\n")

        return {
            "recommended": self._format_items(recommended),
            "good_options": self._format_items(good_options),
            "something_new": self._format_items(something_new),
        }

    def _format_items(self, items):
        output = []
        for i in items:
            act = i["activity"]
            output.append({
                "id": str(act.get("id")),
                "title": str(act.get("title", "Untitled")),
                "description": str(act.get("description", "")),
                "instructions": str(act.get("instructions", "")),
                "emoji": str(act.get("emoji", "🌿")),
                "activity_type": str(act.get("activity_type", "general")),
                "duration": str(act.get("duration", "15")),
                "location": str(act.get("location") or "Indoor"),
                "max_participants": int(act.get("max_participants") or 10),
                "enrolled_count": int(act.get("enrolled") or 1),
                "indoor_outdoor": int(act.get("indoor_outdoor") or 0),
                "energy_required": int(act.get("energy_required") or 0),
                "privacy": int(act.get("privacy") or 0),
                "host_id": act.get("host_id"),
                "host_name": str(act.get("host_name") or "System"),
                "start_date": str(act.get("start_date") or ""),
                "completed_at": act.get("completed_at"),
                "is_canceled": bool(act.get("is_canceled", False)),
                "tags": act.get("tags") if isinstance(act.get("tags"), list) else [],
                "match_score": float(i.get("human_match_score", 0.85)),
                "arm": int(i["arm"]),
                "is_preset": bool(act.get("is_preset", False))
            })
        return output

    def process_feedback_and_learn(self, data):
        before = float(data.get('stress_before', 50))
        after = float(data.get('stress_after', 50))
        rating = float(data.get('rating', 3))
        happiness = float(data.get('happiness', 5.5))
        completed = bool(data.get('completed', False))
        view_time = float(data.get('view_time', 0))

        stress_red = max(0, (before - after) / 100.0)
        rating_score = rating / 5.0
        comp_bonus = 1.0 if completed else 0.0

        res = supabase.table("activities").select("*").eq("id", data['activity_id']).maybe_single().execute()
        activity = res.data
        duration = int(activity.get('duration') or 15) if activity else 15
        engagement = min(view_time / (duration * 60), 1.0)

        reward = (0.45 * stress_red) + (0.30 * rating_score) + (0.15 * comp_bonus) + (0.10 * engagement)

        print("\n" + "═" * 100)
        print(f" 6️⃣  REWARD CALCULATION: How helpful was this activity?")
        print(f"    • Stress: {before} -> {after} | Red: {stress_red:.2f} (x0.45)")
        print(f"    • Rating: {rating}/5        | Scr: {rating_score:.2f} (x0.30)")
        print(f"    • Mood/Happy  : {happiness}/10     | 🌸 (Tracking Only - Already factored into Stress Drop)")
        print(f"    • Status: {'Done' if completed else 'Quit'}      | Bns: {comp_bonus:.2f} (x0.15)")
        print(f"    • Engage: {view_time:.0f}s/{duration}m  | Scr: {engagement:.2f} (x0.10)")
        print(f"    ⭐ FINAL REWARD SIGNAL (r): {reward:.4f}")
        print("-" * 100)

        user_id = data['user_id']
        profile = self._get_user_profile(user_id)
        user_prefs = build_user_preferences(profile)
        history = self._get_user_history(user_id)
        global_stats = self._get_global_stats()

        temp_state = {"stress_score": before, "happiness": rating, "available_time_category": 3, "energy_level": 0.5}
        act_stats = build_activity_stats(profile.get('pref_activities', []), activity, history, global_stats)
        context_vector = build_context_vector(temp_state, user_prefs, activity, act_stats)

        self.bandit.update(0, context_vector, reward)

        from src.bandit.model_registry import save_user_model
        save_user_model(self.user_id, self.bandit)

        print(f" 7️⃣  MODEL UPDATE: Global Shared Weights (θ) updated and synced to Supabase.")
        print(" 🔄 LOOP COMPLETE: The AI is now smarter and the brain is in the cloud.")
        print("═" * 100 + "\n")

        return reward

    def _print_full_21d_trace(self, x, act, state, profile, hist, g_stats):
        names = [
            "stress_norm", "mindful_pref", "phys_pref", "creative_pref", "entert_pref",
            "social_pref", "energy_level", "time_cat_norm", "happy_norm", "loc_pref",
            "tag_similarity", "tag_match_ratio", "novelty_bonus", "rep_penalty",
            "is_mindful", "is_physical", "is_creative", "is_entert", "dur_norm", "pop_score", "loc_numeric"
        ]

        aid = str(act.get('id'))
        seen = hist.get("times_seen", {}).get(aid, 0)
        dur = int(act.get('duration') or 15)

        # 🚀 UPDATE: Grab the enrolled count for the print trace!
        act_enrolled = int(act.get('enrolled', 0))

        for i in range(21):
            val = x[i]
            calc = "Binary/Static Map"
            if i == 0:
                calc = f"{state.get('stress_score')} / 100"
            elif 1 <= i <= 4:
                cat = ["mindfulness", "physical", "creative", "entertainment"][i - 1]
                calc = f"Profile.contains({cat})"
            elif i == 5:
                calc = f"Profile Social Map"
            elif i == 6:
                calc = f"{state.get('energy_level', 0.5)} (Raw)"
            elif i == 7:
                calc = f"{state.get('available_time_category')} / 5"
            elif i == 8:
                # 🚀 Changed from 5 to 10
                calc = f"{state.get('happiness')} / 10"
            elif i == 9:
                calc = f"User Loc Pref ({state.get('location_preference')})"
            elif i == 10:
                calc = f"Jaccard Similarity (Tags)"
            elif i == 11:
                calc = f"Common Tags / {len(act.get('tags', []))}"
            elif i == 12:
                calc = f"1 / (1 + {seen} seen)"
            elif i == 13:
                calc = f"RecentCount / 5"
            elif i == 18:
                calc = f"{dur} min / 60"
            elif i == 19:
                calc = f"min({act_enrolled} / 20.0, 1.0)"  # 🚀 UPDATE: Changed the label calculation

            print(f"[{i + 1:02}] | {names[i]:<22} | {calc:<35} | {val:<8.3f}")

    def _get_user_profile(self, uid):
        try:
            res = supabase.table("profiles").select("*").eq("id", uid).maybe_single().execute()
            return res.data if res and hasattr(res, 'data') and res.data else {}
        except:
            return {}

    def _get_user_history(self, uid):
        try:
            res = supabase.table("user_activity_interactions").select("activity_id").eq("user_id", uid).execute()
            counts = {}
            for r in (res.data if res.data else []):
                aid = str(r['activity_id'])
                counts[aid] = counts.get(aid, 0) + 1
            return {"times_seen": counts}
        except:
            return {"times_seen": {}}

    def _get_global_stats(self):
        try:
            res = supabase.table("user_activity_interactions").select("activity_id").gte("rating", 4).order(
                "created_at", desc=True).limit(100).execute()
            counts = {}
            for r in (res.data if res.data else []):
                aid = str(r['activity_id'])
                counts[aid] = counts.get(aid, 0) + 1
            return {"avg_reward": counts}
        except:
            return {"avg_reward": {}}