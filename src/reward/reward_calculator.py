def calculate_reward(
    stress_before,
    stress_after,
    rating,
    completion,
    view_time_seconds
):

    # Stress reduction
    stress_reduction = max(0, stress_before - stress_after)
    normalized_stress = stress_reduction / 100

    # Rating
    normalized_rating = rating / 5

    # Completion
    normalized_completion = completion / 2

    # View time
    if view_time_seconds > 120:
        normalized_view_time = 0
    else:
        normalized_view_time = min(view_time_seconds / 60, 1)

    reward = (
        0.45 * normalized_stress +
        0.30 * normalized_rating +
        0.15 * normalized_completion +
        0.10 * normalized_view_time
    )

    return reward