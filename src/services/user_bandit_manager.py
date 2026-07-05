from src.bandit.linucb import LinUCB


class UserBanditManager:

    def __init__(self, n_arms, context_dim):

        self.models = {}
        self.n_arms = n_arms
        self.context_dim = context_dim

    def get_model(self, user_id):

        if user_id not in self.models:

            self.models[user_id] = LinUCB(
                self.n_arms,
                self.context_dim
            )

        return self.models[user_id]