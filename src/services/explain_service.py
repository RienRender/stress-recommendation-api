import numpy as np

def explain_recommendation(user_state, activity, context, bandit, arm):

    try:
        # ✅ context is LIST (vector)
        stress = context[0]
        energy = context[1]

        explanation = []

        if stress > 0.6:
            explanation.append("you seem stressed")

        if energy < 0.4:
            explanation.append("you have low energy")

        if activity.get("tags"):
            explanation.append(f"this matches your interest in {activity['tags'][0]}")

        if not explanation:
            return "Recommended based on your behavior"

        return "Recommended because " + ", ".join(explanation)

    except Exception as e:
        print("Explain failure:", e)
        return "Recommended based on your current state"