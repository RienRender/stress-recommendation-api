import random


class ColdStartStrategy:

    def __init__(self, catalog):
        self.catalog = catalog

    def recommend(self, user_state):

        preferences = {
            "mindfulness": user_state.get("mindfulness_preference", 0),
            "physical": user_state.get("physical_preference", 0),
            "creative": user_state.get("creative_preference", 0),
            "entertainment": user_state.get("entertainment_preference", 0)
        }

        best_tag = max(preferences, key=preferences.get)

        candidates = [
            a for a in self.catalog.activities
            if best_tag in a["tags"]
        ]

        if not candidates:
            candidates = self.catalog.activities

        activity = random.choice(candidates)

        return activity["id"], activity