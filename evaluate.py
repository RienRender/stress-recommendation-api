from src.evaluation.replay_evaluator import ReplayEvaluator

evaluator = ReplayEvaluator("logs/replay_dataset.csv")

evaluator.report()