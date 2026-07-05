import numpy as np
from src.bandit.linucb import LinUCB


def test_linucb():

    bandit = LinUCB(5, 8)

    context = np.random.rand(8)

    arm = bandit.select_arm(context)

    assert arm >= 0