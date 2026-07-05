import csv
import os


class ReplayLogger:

    def __init__(self, file_path="replay_log.csv"):

        self.file_path = file_path

        # in-memory dataset for experiments
        self.data = []

        file_exists = os.path.isfile(file_path)

        self.file = open(file_path, "a", newline="")
        self.writer = csv.writer(self.file)

        if not file_exists:
            self.writer.writerow([
                "timestamp",
                "user_id",
                "activity_id",
                "stress",
                "energy",
                "time",
                "reward"
            ])

    def log(self, data):

        # store in memory (used by experiments)
        self.data.append(data)

        # store in CSV (persistent logging)
        self.writer.writerow([
            data["timestamp"],
            data["user_id"],
            data["activity_id"],
            data["stress"],
            data["energy"],
            data["time"],
            data["reward"]
        ])