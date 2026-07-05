import pandas as pd


class ReplayEvaluator:

    def __init__(self, dataset_path):
        self.data = pd.read_csv(dataset_path)

    def average_reward(self):
        return self.data["reward"].mean()

    def engagement_rate(self):
        return (self.data["view_time"] > 10).mean()

    def novelty_average(self):
        return self.data["novelty_bonus"].mean()

    def report(self):

        print("Replay Evaluation Results")
        print("-------------------------")

        print("Average Reward:", self.average_reward())
        print("Engagement Rate:", self.engagement_rate())
        print("Average Novelty:", self.novelty_average())