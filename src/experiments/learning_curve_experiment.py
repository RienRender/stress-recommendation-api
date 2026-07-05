class LearningCurveExperiment:

    def __init__(self):
        self.rewards = []
        self.cumulative_rewards = []

    def log(self, reward):

        self.rewards.append(reward)

        if not self.cumulative_rewards:
            self.cumulative_rewards.append(reward)
        else:
            self.cumulative_rewards.append(
                self.cumulative_rewards[-1] + reward
            )

    def summary(self):

        if len(self.rewards) == 0:
            print("No learning data yet.")
            return

        avg = sum(self.rewards) / len(self.rewards)

        print("\nLearning Curve Experiment\n")
        print("Average Reward:", avg)
        print("Total Interactions:", len(self.rewards))