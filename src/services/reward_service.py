def calculate_reward(
    stress_before,
    stress_after,
    rating,
    completed,
    view_time,
    duration
):
    # 🔹 1. Stress reduction (MAIN SIGNAL)
    stress_reduction = max(0, stress_before - stress_after) / 100

    # 🔹 2. Completion bonus
    completion_bonus = 0.3 if completed else 0.0

    # 🔹 3. Rating (1–5 → 0–1)
    rating_score = (rating or 3) / 5

    # 🔹 4. Engagement (watch time)
    engagement = min(view_time / duration, 1.0) if duration else 0

    # ✅ FINAL REWARD
    reward = (
        0.5 * stress_reduction +
        0.2 * completion_bonus +
        0.2 * rating_score +
        0.1 * engagement
    )

    return reward