import requests
import random
import time

BASE_URL = "http://127.0.0.1:8000"

# ------------------------
# Simulated user profile
# ------------------------
def generate_user_state():
    return {
        "user_id": 1,
        "stress_score": random.randint(40, 90),
        "available_time": random.choice([5, 10, 15]),
        "energy_level": random.choice([0, 1]),
        "social_preference": random.choice([0, 1])
    }


# ------------------------
# Simulated user behavior
# ------------------------
def simulate_feedback(state, activity_name):

    stress_before = state["stress_score"]

    # Activity effectiveness logic
    if activity_name == "Deep Breathing":
        stress_after = stress_before - random.randint(10, 25)
    elif activity_name == "Short Walk":
        stress_after = stress_before - random.randint(5, 20)
    elif activity_name == "Call a Friend":
        stress_after = stress_before - random.randint(5, 15)
    else:
        stress_after = stress_before - random.randint(0, 10)

    stress_after = max(0, stress_after)

    return {
        "stress_before": stress_before,
        "stress_after": stress_after,
        "rating": random.randint(3, 5),
        "view_time": random.randint(10, 60),
        "completed": random.choice([True, True, False]),
        "duration": random.choice([5, 10, 15])
    }


# ------------------------
# MAIN LOOP
# ------------------------
def run_simulation(steps=100):

    rewards = []

    for step in range(steps):

        # 1. Generate user state
        state = generate_user_state()

        # 2. Call recommend API
        res = requests.post(f"{BASE_URL}/recommend", json=state)

        print("STATUS:", res.status_code)
        print("RAW RESPONSE:", res.text)

        rec = res.json()

        activity = rec["activity"]
        arm = rec["arm"]
        context = rec["context"]

        # 3. Simulate feedback
        feedback = simulate_feedback(state, activity)

        # 4. Send feedback API
        feedback_payload = {
            "user_id": state["user_id"],
            "activity_id": arm,
            "arm": arm,
            "context": context,
            **feedback
        }

        res2 = requests.post(f"{BASE_URL}/activity-feedback", json=feedback_payload)
        reward = res2.json()["reward"]

        rewards.append(reward)

        print(f"Step {step+1}")
        print(f"Recommended: {activity}")
        print(f"Reward: {reward}")
        print("-" * 30)

        time.sleep(0.1)  # optional delay

    print("\nAverage Reward:", sum(rewards)/len(rewards))


if __name__ == "__main__":
    run_simulation(100)

import matplotlib.pyplot as plt

plt.plot(rewards)
plt.xlabel("Steps")
plt.ylabel("Reward")
plt.title("Learning Curve")
plt.show()