import numpy as np

# -----------------------
# 1. CTR
# -----------------------
def compute_ctr(interactions):
    # interactions = [{clicked: 0/1}]
    if not interactions:
        return 0
    return sum(i["clicked"] for i in interactions) / len(interactions)


# -----------------------
# 2. Average Reward
# -----------------------
def compute_avg_reward(interactions):
    # interactions = [{reward: float}]
    if not interactions:
        return 0
    return sum(i["reward"] for i in interactions) / len(interactions)


# -----------------------
# 3. Diversity (intra-list)
# -----------------------
def compute_diversity(top_k, similarity_fn):
    if len(top_k) <= 1:
        return 0

    sims = []

    for i in range(len(top_k)):
        for j in range(i + 1, len(top_k)):
            sim = similarity_fn(
                top_k[i]["activity"],
                top_k[j]["activity"]
            )
            sims.append(sim)

    if not sims:
        return 0

    return 1 - np.mean(sims)  # higher = more diverse


# -----------------------
# 4. Novelty
# -----------------------
def compute_novelty(top_k):
    scores = []

    for item in top_k:
        view_count = item["activity"].get("view_count", 0)
        scores.append(1 / (1 + view_count))

    if not scores:
        return 0

    return np.mean(scores)