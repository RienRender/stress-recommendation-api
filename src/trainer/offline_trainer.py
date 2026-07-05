import json
import numpy as np

from src.bandit.linucb import LinUCB
from src.storage.model_store import ModelStore


class OfflineTrainer:

    def __init__(self):

        self.log_file = "data/logs/interactions.jsonl"

        self.n_arms = 5
        self.context_dim = 8

        self.bandit = LinUCB(
            n_arms=self.n_arms,
            context_dim=self.context_dim,
            alpha=0.3
        )

        self.model_store = ModelStore()

    def train(self):

        print("Starting offline training...")

        count = 0

        with open(self.log_file, "r") as f:

            for line in f:

                record = json.loads(line)

                context = np.array(record["context"])

                arm = record["activity_id"]

                # Simulated reward
                reward = np.random.random()

                self.bandit.update(arm, context, reward)

                count += 1

        print(f"Trained on {count} interactions")

        self.model_store.save(self.bandit)

        print("Model saved successfully")


if __name__ == "__main__":

    trainer = OfflineTrainer()
    trainer.train()