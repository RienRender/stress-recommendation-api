import numpy as np

class ReplayEvaluator:

    def __init__(self, dataset):
        self.dataset = dataset

    def evaluate_random_policy(self):

        rewards = []

        for row in self.dataset:

            if np.random.rand() < 0.5:
                rewards.append(row["reward"])

        if len(rewards) == 0:
            return 0

        return sum(rewards) / len(rewards)

    def evaluate_logged_policy(self):

        rewards = [row["reward"] for row in self.dataset]

        return sum(rewards) / len(rewards)