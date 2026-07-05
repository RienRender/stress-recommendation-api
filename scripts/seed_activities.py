import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.config.supabase_client import supabase

activities = [

    # 🧘 MINDFULNESS
    {
        "title": "Deep Breathing Exercise",
        "description": "Slow breathing to relax",
        "activity_type": "mindfulness",
        "duration": 5,
        "difficulty": 0,
        "tags": {
            "category": ["breathing","relaxation","focus"],
            "features": {"mindfulness": 1.0, "physical": 0.0, "creative": 0.0, "entertainment": 0.0},
            "context": {"indoor": 1, "energy_required": 0, "time_category": 1},
            "novelty_score": 0.2
        }
    },
    {
        "title": "5-Minute Meditation",
        "description": "Quick mindfulness meditation",
        "activity_type": "mindfulness",
        "duration": 5,
        "difficulty": 0,
        "tags": {
            "category": ["meditation","calm","focus"],
            "features": {"mindfulness": 1.0, "physical": 0.0, "creative": 0.0, "entertainment": 0.0},
            "context": {"indoor": 1, "energy_required": 0, "time_category": 1},
            "novelty_score": 0.3
        }
    },

    # 🏃 PHYSICAL
    {
        "title": "Light Stretching",
        "description": "Simple body stretching",
        "activity_type": "physical",
        "duration": 10,
        "difficulty": 1,
        "tags": {
            "category": ["stretch","body","relax"],
            "features": {"mindfulness": 0.2, "physical": 0.8, "creative": 0.0, "entertainment": 0.0},
            "context": {"indoor": 1, "energy_required": 1, "time_category": 2},
            "novelty_score": 0.3
        }
    },
    {
        "title": "Short Walk",
        "description": "Walk outside for fresh air",
        "activity_type": "physical",
        "duration": 15,
        "difficulty": 1,
        "tags": {
            "category": ["walk","outdoor","fresh_air"],
            "features": {"mindfulness": 0.3, "physical": 0.7, "creative": 0.0, "entertainment": 0.1},
            "context": {"indoor": 0, "energy_required": 1, "time_category": 2},
            "novelty_score": 0.4
        }
    },

    # 🎨 CREATIVE
    {
        "title": "Journaling",
        "description": "Write your thoughts",
        "activity_type": "creative",
        "duration": 10,
        "difficulty": 0,
        "tags": {
            "category": ["writing","reflection","emotion"],
            "features": {"mindfulness": 0.4, "physical": 0.0, "creative": 1.0, "entertainment": 0.2},
            "context": {"indoor": 1, "energy_required": 0, "time_category": 2},
            "novelty_score": 0.5
        }
    },
    {
        "title": "Sketch Drawing",
        "description": "Draw anything freely",
        "activity_type": "creative",
        "duration": 15,
        "difficulty": 1,
        "tags": {
            "category": ["drawing","art","creativity"],
            "features": {"mindfulness": 0.2, "physical": 0.0, "creative": 1.0, "entertainment": 0.3},
            "context": {"indoor": 1, "energy_required": 1, "time_category": 2},
            "novelty_score": 0.6
        }
    },

    # 🎮 ENTERTAINMENT
    {
        "title": "Watch a Funny Video",
        "description": "Boost mood with humor",
        "activity_type": "entertainment",
        "duration": 5,
        "difficulty": 0,
        "tags": {
            "category": ["fun","video","laugh"],
            "features": {"mindfulness": 0.0, "physical": 0.0, "creative": 0.0, "entertainment": 1.0},
            "context": {"indoor": 1, "energy_required": 0, "time_category": 1},
            "novelty_score": 0.3
        }
    },
    {
        "title": "Listen to Music",
        "description": "Relax with music",
        "activity_type": "entertainment",
        "duration": 10,
        "difficulty": 0,
        "tags": {
            "category": ["music","relax","mood"],
            "features": {"mindfulness": 0.2, "physical": 0.0, "creative": 0.1, "entertainment": 0.9},
            "context": {"indoor": 1, "energy_required": 0, "time_category": 2},
            "novelty_score": 0.4
        }
    },

    # 🧑‍🤝‍🧑 SOCIAL
    {
        "title": "Call a Friend",
        "description": "Talk with someone you trust",
        "activity_type": "social",
        "duration": 10,
        "difficulty": 0,
        "tags": {
            "category": ["social","talk","support"],
            "features": {"mindfulness": 0.3, "physical": 0.0, "creative": 0.0, "entertainment": 0.4},
            "context": {"indoor": 1, "energy_required": 1, "time_category": 2},
            "novelty_score": 0.5
        }
    },

    # ⚡ HIGH ENERGY
    {
        "title": "Quick Workout",
        "description": "Short intense exercise",
        "activity_type": "physical",
        "duration": 10,
        "difficulty": 2,
        "tags": {
            "category": ["exercise","fitness","energy"],
            "features": {"mindfulness": 0.1, "physical": 1.0, "creative": 0.0, "entertainment": 0.2},
            "context": {"indoor": 1, "energy_required": 2, "time_category": 2},
            "novelty_score": 0.6
        }
    }

]

def seed():
    supabase.table("activities").insert(activities).execute()

if __name__ == "__main__":
    seed()