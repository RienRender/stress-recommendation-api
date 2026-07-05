import pandas as pd


def run_replay():

    df = pd.read_csv("logs/replay_dataset.csv")

    if len(df) == 0:
        print("No data available.")
        return

    # CTR
    ctr = (df["reward"] > 0).mean()

    # Average reward
    avg_reward = df["reward"].mean()

    # Engagement score
    engagement = (df["view_time"] * df["view_count"]).mean()

    # Interest alignment
    interest_alignment = df["interest_score"].mean()

    print("=== Replay Evaluation Results ===")
    print(f"CTR: {ctr:.3f}")
    print(f"Average Reward: {avg_reward:.3f}")
    print(f"Engagement Score: {engagement:.3f}")
    print(f"Interest Alignment: {interest_alignment:.3f}")


if __name__ == "__main__":
    run_replay()