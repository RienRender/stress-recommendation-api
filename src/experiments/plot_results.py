import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


# --------------------------------------------------
# Moving average smoothing
# --------------------------------------------------

def moving_average(data, window=50):

    data = np.array(data)

    if len(data) <= window:
        return data

    return np.convolve(data, np.ones(window)/window, mode="valid")


# --------------------------------------------------
# Learning Curve (Alpha comparison)
# --------------------------------------------------

def plot_learning_curves(reward_dict):

    plt.figure(figsize=(10,6))

    for alpha, rewards in reward_dict.items():

        if len(rewards) == 0:
            continue

        smooth = moving_average(rewards, window=50)

        plt.plot(smooth, label=f"α={alpha}")

    plt.xlabel("Interaction Step")
    plt.ylabel("Average Reward")
    plt.title("LinUCB Learning Curve (Smoothed)")

    plt.legend()
    plt.grid(True)

    plt.savefig("learning_curve.png")

    print("Learning curve saved as learning_curve.png")


# --------------------------------------------------
# Cumulative Reward
# --------------------------------------------------

def plot_cumulative_reward(bandit_rewards, baseline_rewards):

    bandit = np.array(bandit_rewards)
    baseline = np.array(baseline_rewards)

    # Fix line stopping issue
    min_len = min(len(bandit), len(baseline))

    bandit = bandit[:min_len]
    baseline = baseline[:min_len]

    bandit_cum = np.cumsum(bandit)
    baseline_cum = np.cumsum(baseline)

    plt.figure(figsize=(10,6))

    plt.plot(bandit_cum, label="LinUCB Bandit")
    plt.plot(baseline_cum, label="Random Baseline")

    plt.title("Cumulative Reward Comparison")
    plt.xlabel("Interaction Step")
    plt.ylabel("Cumulative Reward")

    plt.legend()
    plt.grid(True)

    plt.savefig("cumulative_reward.png")

    print("Cumulative reward graph saved as cumulative_reward.png")


# --------------------------------------------------
# Regret Curve
# --------------------------------------------------

def plot_regret(bandit_regrets, baseline_regrets):

    bandit = np.array(bandit_regrets)
    baseline = np.array(baseline_regrets)

    min_len = min(len(bandit), len(baseline))

    bandit = bandit[:min_len]
    baseline = baseline[:min_len]

    bandit_cum = np.cumsum(bandit)
    baseline_cum = np.cumsum(baseline)

    plt.figure(figsize=(10,6))

    plt.plot(bandit_cum, label="LinUCB Bandit")
    plt.plot(baseline_cum, label="Random Baseline")

    plt.title("Cumulative Regret Comparison")
    plt.xlabel("Interaction Step")
    plt.ylabel("Total Regret")

    plt.legend()
    plt.grid(True)

    plt.savefig("regret_curve.png")

    print("Regret curve saved as regret_curve.png")