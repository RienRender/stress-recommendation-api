import numpy as np


class FeatureBuilder:

    def build(self, user_state):

        # -------- NORMALIZATION --------
        stress = user_state.get("stress_score", 0) / 100
        time_available = user_state.get("available_time", 0) / 30
        energy = user_state.get("energy_level", 0) / 2
        social = user_state.get("social_preference", 0) / 2

        # -------- PREFERENCES --------
        mindfulness = user_state.get("mindfulness_preference", 0)
        physical = user_state.get("physical_preference", 0)
        creative = user_state.get("creative_preference", 0)
        entertainment = user_state.get("entertainment_preference", 0)

        # -------- BASE CONTEXT --------
        return np.array([
            stress,
            time_available,
            energy,
            social,
            mindfulness,
            physical,
            creative,
            entertainment
        ])