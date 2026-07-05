import json
from datetime import datetime
import os


class EventLogger:

    def __init__(self):

        self.path = "data/logs/events.jsonl"

        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def log(self, event):

        event["timestamp"] = datetime.utcnow().isoformat()

        with open(self.path, "a") as f:

            f.write(json.dumps(event) + "\n")