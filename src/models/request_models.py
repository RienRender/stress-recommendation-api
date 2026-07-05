from pydantic import BaseModel, field_validator
from typing import List, Optional, Union, Dict, Any  # 🚀 THE FIX: Added Dict and Any here!
import numpy as np


class RecommendRequest(BaseModel):
    user_id: Union[str, int]
    stress_score: float
    energy_level: float
    available_time_category: int
    social_preference: float = 0.0
    happiness: float = 0.5
    location_preference: int = 0

    # 🚀 THE OVERRIDES
    energy_override: Optional[int] = None
    social_override: Optional[int] = None
    time_override: Optional[int] = None
    location_override: Optional[int] = None

    # 🚀 THE ACTIVITY POOL
    activity_pool: Optional[List[Dict[str, Any]]] = []


class FeedbackRequest(BaseModel):
    user_id: str
    activity_id: int
    stress_before: float
    stress_after: float
    rating: float
    happiness: float = 5.5
    completed: bool
    view_time: float
    context: List[float]
    arm: int

    @field_validator("activity_id")
    def ensure_int(cls, v):
        if isinstance(v, (list, np.ndarray)):
            return int(v[0])
        return int(v)