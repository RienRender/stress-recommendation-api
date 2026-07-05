import json
from datetime import datetime
import os


class RewardLogger:

    def __init__(self):

        self.path = "data/logs/rewards.jsonl"

        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def log(self, record: dict):

        record["timestamp"] = datetime.utcnow().isoformat()

        with open(self.path, "a") as f:

            f.write(json.dumps(record) + "\n")