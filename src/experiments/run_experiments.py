from src.experiments.alpha_experiment import AlphaExperiment
from src.experiments.learning_curve_experiment import LearningCurveExperiment
from src.experiments.diversity_experiment import DiversityExperiment
from src.experiments.metrics_tracker import MetricsTracker
from .baseline_experiment import BaselineExperiment
from src.experiments.cold_start_experiment import ColdStartExperiment


class ExperimentRunner:

    def __init__(self, bandits):

        self.alpha = AlphaExperiment(bandits)
        self.learning = LearningCurveExperiment()
        self.diversity = DiversityExperiment()
        self.metrics = MetricsTracker()
        self.baseline = BaselineExperiment()
        self.cold_start = ColdStartExperiment()

    def log(self, alpha, activity_id, reward):

        self.alpha.log(alpha, reward)
        self.learning.log(reward)
        self.diversity.log(activity_id)
        self.metrics.log(reward)

    def summary(self):

        self.alpha.summary()
        self.learning.summary()
        self.diversity.summary()
        self.metrics.summary()
        self.baseline.summary()