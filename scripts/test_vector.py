from src.utils.feature_engineering import build_activity_vector

activity = {
    "tags": {
        "features": {"mindfulness": 1.0},
        "context": {"indoor": 1, "energy_required": 0, "time_category": 1},
        "novelty_score": 0.2
    }
}

print(build_activity_vector(activity))