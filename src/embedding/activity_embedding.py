import random


class ActivityEmbedding:

    def embed(self, text):
        """
        text = activity name + tags
        Returns simple numeric embedding
        """

        words = text.lower().split()

        embedding = [0] * 5

        for i, word in enumerate(words):
            embedding[i % 5] += len(word)

        # normalize
        total = sum(embedding) + 1e-6
        embedding = [v / total for v in embedding]

        return embedding