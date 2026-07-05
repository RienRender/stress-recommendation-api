import numpy as np
import time
import random

from src.logging.replay_logger import ReplayLogger
from src.bandit.linucb import LinUCB
from src.features.feature_builder import FeatureBuilder
from src.activities.activity_catalog import ActivityCatalog
from src.logging.interaction_logger import InteractionLogger
from src.storage.model_store import ModelStore
from src.coldstart.cold_start import ColdStartStrategy
from src.recommendation.candidate_generator import CandidateGenerator

from src.experiments.run_experiments import ExperimentRunner
from src.experiments.alpha_experiment import AlphaExperiment
from src.experiments.plot_results import plot_learning_curves
from src.experiments.plot_results import plot_cumulative_reward
from src.experiments.plot_results import plot_regret
from src.experiments.replay_evaluation import ReplayEvaluator
from src.experiments.policy_heatmap import plot_policy_heatmap


# --------------------------------------------------
# Simulated Reward Function
# --------------------------------------------------

def simulate_reward(activity_id, stress, energy):

    base = random.uniform(0.2, 0.4)

    if activity_id == 1 and stress > 60:
        base += 0.4

    elif activity_id == 2 and energy == 0:
        base += 0.4

    elif activity_id == 3 and energy >= 1:
        base += 0.3

    elif activity_id == 4:
        base += 0.2

    return min(base, 1.0)


# --------------------------------------------------
# Recommendation Service
# --------------------------------------------------

class RecommendationService:

    def __init__(self):

        self.features = FeatureBuilder()
        self.catalog = ActivityCatalog()

        self.model_store = ModelStore()
        self.logger = InteractionLogger()
        self.replay_logger = ReplayLogger()

        self.cold_start = ColdStartStrategy(self.catalog)
        self.candidates = CandidateGenerator(self.catalog)

        # -----------------------------
        # Bandit Setup
        # -----------------------------

        n_arms = len(self.catalog.activities)
        context_dim = 14

        self.bandits = {
            0.1: LinUCB(n_arms, context_dim, alpha=0.1),
            0.3: LinUCB(n_arms, context_dim, alpha=0.3),
            0.5: LinUCB(n_arms, context_dim, alpha=0.5),
            0.7: LinUCB(n_arms, context_dim, alpha=0.7)
        }

        self.alpha_experiment = AlphaExperiment(self.bandits)
        self.experiments = ExperimentRunner(self.bandits)

        # -----------------------------
        # Arm mapping
        # -----------------------------

        self.id_to_arm = {}
        self.arm_to_id = {}

        for i, activity in enumerate(self.catalog.activities):

            self.id_to_arm[activity["id"]] = i
            self.arm_to_id[i] = activity["id"]

    # --------------------------------------------------
    # Recommendation
    # --------------------------------------------------

    def recommend(self, user_state):

        context = self.features.build_context(user_state)

        if user_state.get("user_id") is None:
            arm, activity = self.cold_start.recommend(user_state)

            reward = simulate_reward(
                activity["id"],
                user_state.get("stress_score", 50),
                user_state.get("energy_level", 1)
            )

            self.experiments.cold_start.log(reward)

            return arm, activity

        candidates = self.candidates.generate(user_state)

        best_score = -1e9
        best_arm = None
        best_alpha = None
        best_context = None
        best_activity = None

        # -----------------------------
        # Bandit prediction
        # -----------------------------

        for a in candidates:

            activity_id = a["id"]
            arm = self.id_to_arm[activity_id]

            embedding = np.array(a["embedding"])
            full_context = np.concatenate([context, embedding])

            novelty = self.novelty_bonus(arm)

            for alpha, bandit in self.bandits.items():

                score = bandit.predict(arm, full_context) + novelty

                if score > best_score:

                    best_score = score
                    best_arm = arm
                    best_alpha = alpha
                    best_context = full_context
                    best_activity = a

        activity_id = self.arm_to_id[best_arm]

        # -----------------------------
        # Simulated Feedback
        # -----------------------------

        stress = user_state.get("stress_score", 50)
        energy = user_state.get("energy_level", 1)

        reward = simulate_reward(activity_id, stress, energy)

        # -----------------------------
        # Bandit metrics
        # -----------------------------

        self.experiments.metrics.log(reward)
        self.experiments.learning.log(reward)

        # -----------------------------
        # Baseline experiment
        # -----------------------------

        baseline_activity = random.choice(self.catalog.activities)

        baseline_reward = simulate_reward(
            baseline_activity["id"],
            stress,
            energy
        )

        self.experiments.baseline.log(baseline_reward)

        # -----------------------------
        # Alpha experiment
        # -----------------------------

        self.alpha_experiment.log(best_alpha, reward)

        self.experiments.log(best_alpha, activity_id, reward)

        # -----------------------------
        # Update bandit
        # -----------------------------

        selected_bandit = self.bandits[best_alpha]
        selected_bandit.update(best_arm, best_context, reward)

        # -----------------------------
        # Replay dataset
        # -----------------------------

        self.replay_logger.log({

            "timestamp": time.time(),
            "user_id": user_state.get("user_id", 0),
            "activity_id": activity_id,
            "stress": stress,
            "energy": energy,
            "time": user_state.get("available_time", 10),
            "reward": reward

        })

        # -----------------------------
        # Interaction log
        # -----------------------------

        self.logger.log({

            "user_id": user_state.get("user_id", 0),
            "context": context.tolist(),
            "activity_id": activity_id

        })

        return best_arm, best_activity

    # --------------------------------------------------

    def novelty_bonus(self, arm):

        return random.uniform(0.01, 0.05)

    # --------------------------------------------------
    # Experiment Results
    # --------------------------------------------------

    def experiment_results(self):

        print("\n===== Experiment Results =====\n")

        self.alpha_experiment.summary()
        self.experiments.summary()

        # Graphs

        plot_learning_curves(self.alpha_experiment.rewards)

        plot_cumulative_reward(
            self.experiments.metrics.rewards,
            self.experiments.baseline.rewards
        )

        plot_regret(
            self.experiments.metrics.regrets,
            self.experiments.baseline.regrets
        )

        plot_policy_heatmap(self.replay_logger.data)
        
        self.experiments.cold_start.summary()


        # -----------------------------
        # Replay Evaluation
        # -----------------------------

        dataset = self.replay_logger.data

        if dataset:

            evaluator = ReplayEvaluator(dataset)

            logged_score = evaluator.evaluate_logged_policy()
            random_score = evaluator.evaluate_random_policy()

            print("\nReplay Evaluation")

            print("Logged Policy Reward:", round(logged_score, 3))
            print("Random Policy Reward:", round(random_score, 3))