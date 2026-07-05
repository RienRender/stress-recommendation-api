import random
from src.recommendation.recommendation_service import RecommendationService

recommender = RecommendationService()


def simulate_user_response(activity):

    tags = activity.get("tags", [])

    # More realistic mixed preferences
    base = 0.4

    if "breathing" in tags:
        base += 0.3

    if "music" in tags:
        base += 0.2

    if "exercise" in tags:
        base += 0.1

    # Add randomness
    reward = min(1.0, max(0.0, base + random.uniform(-0.2, 0.2)))

    return {
        "stress_after": random.randint(20, 70),
        "rating": int(reward * 5),
        "view_time": random.randint(100, 400),
        "completed": reward > 0.5,
        "reward": reward
    }


def run_simulation():
    
    rewards = []

    user_state = {
        "user_id": 1,
        "stress_score": 70,
        "available_time": 10,
        "energy_level": 1,
        "social_preference": 0
    }

    for step in range(100):

        activity, arm, context = recommender.recommend_activity(user_state)

        result = simulate_user_response(activity)

        recommender.update_from_feedback(
            arm,
            context,
            result["reward"]
        )

        rewards.append(result["reward"])

        print(f"Step {step+1}")
        print("Recommended:", activity["name"])
        print("Reward:", result["reward"])
        print("-" * 30)

    print("\nAverage Reward:", sum(rewards) / len(rewards))

    return rewards


if __name__ == "__main__":
    rewards = run_simulation()

    import matplotlib.pyplot as plt

    plt.plot(rewards)
    plt.title("Learning Curve")
    plt.xlabel("Steps")
    plt.ylabel("Reward")
    plt.show()