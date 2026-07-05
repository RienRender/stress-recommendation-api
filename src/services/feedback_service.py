from src.reward.reward_calculator import RewardCalculator
from src.recommendation.recommendation_service import RecommendationService
from src.logging.reward_logger import RewardLogger
from src.services.tag_service import get_activity_tags
from src.services.tag_preference_service import update_user_tag, update_global_tag



class FeedbackService:

    def __init__(self):

        self.reward_calc = RewardCalculator()
        self.recommendation = RecommendationService()
        self.logger = RewardLogger()

    def process_feedback(self, data):
        reward = self.reward_calc.calculate(data)

        arm = data["activity_id"]

        user_state = data["user_state"]

        self.recommendation.update(arm, user_state, reward)

        self.logger.log({
            "user_id": user_state.get("user_id", 0),
            "activity_id": arm,
            "reward": reward
        })

        tags = get_activity_tags(activity_id)

        for tag_id in tags:
            update_user_tag(user_id, tag_id)
            update_global_tag(tag_id)

        return reward