import random


class ColdStartExperiment:

    def __init__(self):
        self.rewards = []
        self.interactions = 0

    def log(self, reward):

        self.rewards.append(reward)
        self.interactions += 1

    def summary(self):

        print("\nCold Start Experiment")

        if self.interactions == 0:
            print("No cold-start data.")
            return

        avg = sum(self.rewards) / self.interactions

        print("Interactions:", self.interactions)
        print("Average Reward:", round(avg, 4))