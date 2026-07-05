import requests
import random
import time

URL = "http://127.0.0.1:8000"


def generate_user():
    return {
        "user_id": 1,
        "stress_score": random.randint(40, 90),
        "energy_level": random.uniform(0.2, 0.8),
        "available_time_category": random.randint(1, 4),
        "social_preference": random.uniform(0, 1),
        "happiness": random.uniform(0, 1),
        "location_preference": random.choice([0, 1, 2])
    }


for i in range(30):
    try:
        user = generate_user()

        rec_raw = requests.post(f"{URL}/recommend", json=user)
        rec = rec_raw.json()

        if "best_match" not in rec:
            print("❌ BAD RESPONSE:", rec)
            continue

        top = rec["best_match"][0]

        print(f"\n[STEP {i}]")
        print("Recommended:", top["activity_name"])

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
        fb_res = fb_raw.json()

        print(f"Reward: {fb_res.get('reward')}")

        time.sleep(1)

    except Exception as e:
        print("❌ SIMULATION ERROR:", e)
        continue


