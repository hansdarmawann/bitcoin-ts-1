import os
import json
import joblib

def load_latest_model(
    model_dir="..\\Models",
    model_key="sarima"
):
    """
    Load latest model and its metadata based on timestamp.
    
    Returns:
        model   : loaded model object
        metadata: dict or None
        model_file: filename of loaded model
    """
    
    # 1. Find model files
    model_files = sorted(
        [
            f for f in os.listdir(model_dir)
            if f.startswith(f"{model_key}_model") and f.endswith(".joblib")
        ],
        reverse=True
    )
    
    if not model_files:
        raise FileNotFoundError(
            f"No model found for key '{model_key}' in {model_dir}"
        )
    
    # 2. Pick latest model
    model_file = model_files[0]
    timestamp = model_file.split("_")[-1].replace(".joblib", "")
    
    model_path = os.path.join(model_dir, model_file)
    model = joblib.load(model_path)
    
    # 3. Load matching metadata (if exists)
    metadata_file = f"{model_key}_metadata_{timestamp}.json"
    metadata_path = os.path.join(model_dir, metadata_file)
    
    metadata = None
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
    
    return model, metadata, model_file
