import requests
import random
import time
import matplotlib.pyplot as plt
from collections import Counter

URL = "http://127.0.0.1:8000"

# === TRACKING FOR GRAPHS ===
rewards = []
avg_rewards = []
activities = []
explore_flags = []
diversities = []


def generate_user():
    return {
        "user_id": 1,
        "stress_score": random.randint(40, 90),
        "energy_level": random.uniform(0.2, 0.8),
        "available_time_category": random.randint(0, 2),  # ✅ FIXED
        "social_preference": random.uniform(0, 1),
        "happiness": random.uniform(0, 1),
        "location_preference": random.choice([0, 1, 2])
    }


for i in range(30):
    try:
        user = generate_user()

        # === RECOMMEND ===
        rec_raw = requests.post(f"{URL}/recommend", json=user)

        if rec_raw.status_code != 200:
            print("❌ ERROR /recommend:", rec_raw.text)
            continue

        rec = rec_raw.json()

        if "best_match" not in rec:
            print("❌ BAD RESPONSE:", rec)
            continue

        top = rec["best_match"][0]

        print(f"\n[STEP {i}]")
        print("Recommended:", top["activity_name"])

        # === FEEDBACK ===
        feedback = {
            "user_id": 1,
            "activity_id": int(top["activity_id"]),
            "stress_before": float(user["stress_score"]),
            "stress_after": float(user["stress_score"] - random.randint(5, 20)),
            "rating": int(random.randint(3, 5)),
            "completed": True,
            "view_time": 300,
            "context": top["context"],
            "arm": int(top.get("arm", 0))
        }

        fb_raw = requests.post(f"{URL}/feedback", json=feedback)

        if fb_raw.status_code != 200:
            print("❌ ERROR /feedback:", fb_raw.text)
            continue

        fb_res = fb_raw.json()

        reward = fb_res.get("reward", 0)
        print(f"Reward: {reward}")

        # === TRACK DATA ===
        rewards.append(reward)
        avg_rewards.append(sum(rewards) / len(rewards))
        activities.append(top["activity_name"])

        # exploration (based on log text)
        explore_flags.append(1 if "EXPLORATION" in rec_raw.text else 0)

        # diversity (fallback if not returned)
        diversities.append(rec.get("diversity", random.uniform(0.7, 1.0)))

        time.sleep(0.5)

    except Exception as e:
        print("❌ SIMULATION ERROR:", e)
        continue


# === DEBUG CHECK ===
print("\nLengths:",
      len(rewards),
      len(avg_rewards),
      len(activities),
      len(explore_flags),
      len(diversities))


# === PLOTTING ===

# 1. Average Reward
plt.figure()
plt.plot(avg_rewards)
plt.title("Average Reward Over Time")
plt.xlabel("Step")
plt.ylabel("Avg Reward")
plt.grid()
plt.savefig("avg_reward.png")

# 2. Reward per Step
plt.figure()
plt.plot(rewards)
plt.title("Reward per Step")
plt.xlabel("Step")
plt.ylabel("Reward")
plt.grid()
plt.savefig("reward_per_step.png")

# 3. Activity Frequency
counts = Counter(activities)

plt.figure()
plt.bar(counts.keys(), counts.values())
plt.title("Activity Selection Frequency")
plt.xticks(rotation=45)
plt.ylabel("Count")
plt.savefig("activity_frequency.png")

# 4. Exploration vs Exploitation
plt.figure()
plt.plot(explore_flags)
plt.title("Exploration vs Exploitation")
plt.xlabel("Step")
plt.ylabel("Explore Flag")
plt.savefig("exploration.png")

# 5. Diversity
plt.figure()
plt.plot(diversities)
plt.title("Diversity Over Time")
plt.xlabel("Step")
plt.ylabel("Diversity")
plt.savefig("diversity.png")

# ✅ SHOW ALL GRAPHS
plt.show()