import numpy as np
import matplotlib.pyplot as plt

def plot_policy_heatmap(dataset):

    stress_levels = []
    activities = []

    for row in dataset:
        stress_levels.append(row["stress"])
        activities.append(row["activity_id"])

    plt.figure(figsize=(8,6))

    plt.hist2d(stress_levels, activities, bins=[10,4])

    plt.colorbar()

    plt.xlabel("Stress Level")
    plt.ylabel("Recommended Activity")

    plt.title("Policy Behavior Heatmap")

    plt.savefig("policy_heatmap.png")

    print("Policy heatmap saved as policy_heatmap.png")