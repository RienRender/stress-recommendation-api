from collections import defaultdict


class UserInterest:

    def __init__(self):
        self.view_count = defaultdict(int)

    def update(self, user_id, activity_id):

        key = (user_id, activity_id)

        self.view_count[key] += 1

    def get(self, user_id, activity_id):

        return self.view_count.get((user_id, activity_id), 0)