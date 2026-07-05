from pydantic import BaseModel


class UserState(BaseModel):

    stress_score: float
    energy_level: float
    available_time: int
    social_preference: float
    mindfulness_preference: float
    physical_preference: float
    creative_preference: float
    entertainment_preference: float


class FeedbackInput(BaseModel):

    activity_id: int
    completed: int
    stress_reduction: float
    happiness: float
    rating: float
    user_state: dict