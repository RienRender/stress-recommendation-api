import numpy as np
import random
from .base_bandit import BaseBandit


class EpsilonGreedy(BaseBandit):

    def __init__(self, n_arms: int, context_dim: int, epsilon: float = 0.1):
        super().__init__(n_arms, context_dim)

        self.epsilon = epsilon
        self.values = np.zeros(n_arms)
        self.counts = np.zeros(n_arms)

    def select_arm(self, context):

        if random.random() < self.epsilon:
            return random.randint(0, self.n_arms - 1)

        return int(np.argmax(self.values))

    def update(self, arm, context, reward):

        self.counts[arm] += 1
        n = self.counts[arm]

        value = self.values[arm]

        new_value = ((n - 1) / n) * value + (1 / n) * reward

        self.values[arm] = new_value