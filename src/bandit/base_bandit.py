import numpy as np
from abc import ABC, abstractmethod


class BaseBandit(ABC):
    """
    Abstract base class for contextual bandit algorithms.
    """

    def __init__(self, n_arms: int, context_dim: int):
        self.n_arms = n_arms
        self.context_dim = context_dim

    @abstractmethod
    def select_arm(self, context: np.ndarray) -> int:
        """
        Select an arm based on the context.
        """
        pass

    @abstractmethod
    def update(self, arm: int, context: np.ndarray, reward: float):
        """
        Update model parameters based on observed reward.
        """
        pass