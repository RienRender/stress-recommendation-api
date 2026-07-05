import random

class BaselineExperiment:

    def __init__(self):
        self.total_reward = 0
        self.interactions = 0

        self.rewards = []
        self.regrets = []

    def log(self, reward):
        self.total_reward += reward
        self.interactions += 1

        self.rewards.append(reward)

        regret = 1 - reward
        self.regrets.append(regret)

    def summary(self):

        print("\nBaseline Experiment (Random Recommender)")

        if self.interactions == 0:
            print("No baseline data yet.")
            return

        avg = self.total_reward / self.interactions

        print("Interactions:", self.interactions)
        print("Average Reward:", round(avg, 4))