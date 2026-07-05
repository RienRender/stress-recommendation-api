class MetricsTracker:

    def __init__(self):

        self.total_reward = 0
        self.total_regret = 0
        self.interactions = 0

        # NEW
        self.rewards = []
        self.regrets = []

    def log(self, reward):

        regret = 1 - reward

        self.total_reward += reward
        self.total_regret += regret
        self.interactions += 1

        # NEW
        self.rewards.append(reward)
        self.regrets.append(regret)

    def summary(self):

        print("\nSystem Metrics")
        print("Total Interactions:", self.interactions)

        if self.interactions == 0:
            print("Average Reward: No data yet")
            return

        avg_reward = self.total_reward / self.interactions
        print("Average Reward:", round(avg_reward, 3))