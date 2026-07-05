import json
import os
import time
from src.config.supabase_client import supabase


class InteractionLogger:

    def __init__(self):

        self.file = "data/interactions.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)

    def log(self, record):

        record["timestamp"] = time.time()

        self._log_json(record)
        self._log_database(record)

    def _log_json(self, record):

        with open(self.file, "r") as f:
            data = json.load(f)

        data.append(record)

        with open(self.file, "w") as f:
            json.dump(data, f, indent=2)

    def _log_database(self, record):

        try:
            supabase.table("user_activity_interactions").insert({
                "user_id": record.get("user_id"),
                "activity_id": record.get("activity_id"),
                "context": record.get("context"),
                "reward": record.get("reward"),
                "stress_before": record.get("stress_before"),
                "stress_after": record.get("stress_after"),
                "rating": record.get("rating"),
                "view_time": record.get("view_time"),
                "completed": record.get("completed")
            }).execute()

        except Exception as e:
            print("Database logging failed:", e)