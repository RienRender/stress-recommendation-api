class AlphaExperiment:

    def __init__(self, bandits):

        # bandits = {0.1: LinUCB, 0.3: LinUCB, 0.7: LinUCB}
        self.bandits = bandits

        self.rewards = {alpha: [] for alpha in bandits.keys()}

    def log(self, alpha, reward):

        self.rewards[alpha].append(reward)

    def summary(self):

        print("\n===== Alpha Experiment Results =====\n")

        for alpha, rewards in self.rewards.items():

            if len(rewards) == 0:
                continue

            avg_reward = sum(rewards) / len(rewards)

            print("Alpha:", alpha)
            print("Interactions:", len(rewards))
            print("Average Reward:", round(avg_reward, 4))
            print()