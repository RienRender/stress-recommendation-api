import numpy as np
import pickle
import os

MODEL_PATH = "linucb_model.pkl"
CURRENT_VERSION = "v3"  # 🔥 Bumped version so it forces a wipe of old brains


class LinUCB:
    def __init__(self, n_features=21, alpha=1.0, version=CURRENT_VERSION):
        self.version = version
        self.n_features = n_features
        self.alpha = alpha

        # 🚀 THE UPGRADE: A single, global matrix. No more "Arms"!
        self.A = np.identity(n_features, dtype=np.float64)
        self.b = np.zeros(n_features, dtype=np.float64)

    def _ensure_dimensions(self):
        # 🔥 HARD DEFENSE: Ensure the matrices are the exact correct size
        if getattr(self, "A", None) is None or self.A.shape[0] != self.n_features:
            self.A = np.identity(self.n_features, dtype=np.float64)
        if getattr(self, "b", None) is None or self.b.shape[0] != self.n_features:
            self.b = np.zeros(self.n_features, dtype=np.float64)

    @property
    def theta(self):
        # Calculates the weights dynamically based on A and b
        self._ensure_dimensions()
        A_inv = np.linalg.inv(self.A)
        return A_inv @ self.b

    def predict(self, x):
        self._ensure_dimensions()
        x = np.array(x, dtype=np.float64).flatten()

        A_inv = np.linalg.inv(self.A)
        theta = A_inv @ self.b

        # Score = Exploit + Explore
        return float(theta.dot(x) + self.alpha * np.sqrt(x.dot(A_inv).dot(x)))

    def update(self, arm_ignored, context, reward):
        # We still accept 'arm' to not break the API, but we ignore it!
        self._ensure_dimensions()
        x = np.array(context, dtype=np.float64).reshape(-1, 1)

        self.A += x @ x.T
        self.b += reward * x.flatten()


# --- Helper functions for local saves if needed ---
def save_model(model):
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)


def load_model():
    if not os.path.exists(MODEL_PATH):
        return LinUCB()

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    if not hasattr(model, "version") or model.version != CURRENT_VERSION:
        print("🚨 MODEL VERSION MISMATCH → RESETTING TO V3 SHARED MODEL")
        return LinUCB()

    return model