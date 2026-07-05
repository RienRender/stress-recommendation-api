import pickle


class ModelStore:

    def save(self, model):

        with open("models/bandit_model.pkl", "wb") as f:
            pickle.dump(model, f)

    def load(self):

        try:
            with open("models/bandit_model.pkl", "rb") as f:
                return pickle.load(f)
        except:
            return None