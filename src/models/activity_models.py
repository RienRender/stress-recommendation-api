from pydantic import BaseModel
from typing import List


class CreateActivityRequest(BaseModel):
    user_id: int

    title: str
    description: str

    activity_type: str  # mindfulness / physical / creative / entertainment

    energy_required: int  # 0,1,2
    indoor_outdoor: int   # 0 indoor, 1 outdoor
    time_category: int    # 1–5
    estimated_duration: int

    tags: List[str]