import requests
import random

URL = "http://127.0.0.1:8000/recommend"

TOTAL_INTERACTIONS = 2000

for i in range(TOTAL_INTERACTIONS):

    payload = {
        "user_id": random.randint(1,5),
        "stress_score": random.randint(20,80),
        "available_time": random.choice([5,10,15,30]),
        "energy_level": random.randint(0,2),
        "social_preference": random.randint(0,2)
    }

    r = requests.post(URL, json=payload)

    print("Call:", i, "Status:", r.status_code)

print("Requesting experiment results...")

requests.get("http://127.0.0.1:8000/experiment-results")