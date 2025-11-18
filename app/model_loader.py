import os
from app.model import DemandForecaster2026

MODELS = {}

def load_models(models_dir="app/models"):
    """Heavy model loading. Called only when server starts."""
    global MODELS
    try:
        MODELS["regressor"] = DemandForecaster2026(models_dir, "regressor")
        MODELS["classifier"] = DemandForecaster2026(models_dir, "classifier")
        print("✅ Models loaded successfully.")
    except Exception as e:
        print(" Model loading failed:", e)

def get_models():
    """Used by predict route (and monkeypatched in tests)"""
    return MODELS
