from collections import defaultdict


class DiversityExperiment:

    def __init__(self):
        self.activity_counts = defaultdict(int)

    def log(self, activity_id):
        self.activity_counts[activity_id] += 1

    def summary(self):

        unique = len(self.activity_counts)

        print("\nDiversity Experiment\n")

        print("Unique Activities Recommended:", unique)

        print("\nActivity Distribution")

        for k, v in self.activity_counts.items():
            print("Activity", k, ":", v)