import random


class ColdStartStrategy:

    def __init__(self, activities):

        self.activities = activities

    def recommend(self):

        return random.choice(self.activities)