import os
import io
import pickle
from src.bandit.linucb import LinUCB, CURRENT_VERSION
from src.config.supabase_client import supabase

# In-memory cache to keep the model "awake" during a session
models = {}

# Match your 21-D system
N_ARMS = 100
N_FEATURES = 21


def get_model(user_id: str):
    """Retrieves a specific user's model from RAM or Supabase Cloud."""
    user_id = str(user_id)

    # 1. Check RAM (Fastest)
    if user_id in models:
        return models[user_id]

    # 2. Try to LOAD from Supabase Cloud
    model = load_user_model_from_cloud(user_id)

    if model:
        # Check if model version matches current 21-D logic
        if not hasattr(model, "version") or model.version != CURRENT_VERSION:
            print(f"🚨 Version mismatch for {user_id} -> RESETTING")
            model = _create_fresh_model()
    else:
        # 3. Create fresh if doesn't exist in cloud
        print(f"🆕 No cloud model for {user_id} -> Creating fresh")
        model = _create_fresh_model()

    # Store in memory cache
    models[user_id] = model
    return model


def _create_fresh_model():
    # 🚀 THE FIX: Remove n_arms because the brain is now one global shared matrix
    return LinUCB(n_features=N_FEATURES, alpha=1.0, version=CURRENT_VERSION)


def load_user_model_from_cloud(user_id: str):
    """Downloads the .pkl from Supabase Storage."""
    file_path = f"{user_id}.pkl"
    try:
        # Download from 'models' bucket
        response = supabase.storage.from_("models").download(file_path)
        print(f"☁️ Cloud Model Fetched: {file_path}")
        return pickle.loads(response)
    except Exception:
        return None


def save_user_model(user_id: str, model_state):
    """Syncs the model state to Supabase Cloud Storage."""
    user_id = str(user_id)
    file_path = f"{user_id}.pkl"
    try:
        # Convert model object to bytes
        pickled_data = pickle.dumps(model_state)

        # Upload/Overwrite in Supabase
        supabase.storage.from_("models").upload(
            path=file_path,
            file=pickled_data,
            file_options={"cache-control": "3600", "upsert": "true", "x-upsert": "true"}
        )
        # Keep the RAM cache updated too
        models[user_id] = model_state
        print(f"✅ Cloud Model Synced: {file_path}")
    except Exception as e:
        print(f"🚨 Cloud Sync Failed: {e}")


if __name__ == "__main__":
    # Test script to see if Supabase is reachable
    test_id = "test_user_001"
    test_model = {"A": "test", "b": "data"}
    print("Testing cloud sync...")
    save_user_model(test_id, test_model)