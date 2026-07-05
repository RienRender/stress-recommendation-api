import random


class CandidateGenerator:

    def __init__(self, catalog):
        self.catalog = catalog

    def generate(self, user_state):

        activities = self.catalog.activities

        popular = activities[:10]

        tag_pref = max(
            ["mindfulness", "physical", "creative", "entertainment"],
            key=lambda t: user_state.get(f"{t}_preference", 0)
        )

        tag_similar = [
            a for a in activities if tag_pref in a["tags"]
        ][:10]

        unseen = activities[10:20]

        random_set = random.sample(activities, min(10, len(activities)))

        pool = popular + tag_similar + unseen + random_set

        unique = {a["id"]: a for a in pool}

        return list(unique.values())