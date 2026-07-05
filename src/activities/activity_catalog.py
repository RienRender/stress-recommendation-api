from src.data.activity_loader import load_activities

class ActivityCatalog:

    def __init__(self):

        self.activities = load_activities()