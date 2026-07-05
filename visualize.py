import matplotlib.pyplot as plt
import pickle

with open("reward_log.pkl", "rb") as f:
    rewards = pickle.load(f)

plt.plot(rewards)
plt.title("Learning Curve")
plt.xlabel("Interactions")
plt.ylabel("Reward")
plt.show()