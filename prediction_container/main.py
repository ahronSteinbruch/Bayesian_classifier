import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from predictor import Predictor
from cache import Cache
import requests
import time
import os

app = FastAPI()
predictor = Predictor()
cache = Cache()


class PredictionRequest(BaseModel):
    features: Dict[str,Any]


def fetch_and_load_model():
    """Fetches the model from the training service and loads it."""
    trainer_url = os.environ.get("TRAINER_URL", "http://trainer:8080/reload_model")
    max_retries = 5
    retry_delay = 10  # seconds

    for attempt in range(max_retries):
        try:
            print(f"Attempting to fetch model from trainer (Attempt {attempt + 1}/{max_retries})...", flush=True)
            response = requests.get(trainer_url)
            response.raise_for_status()  # Raises HTTPError for bad responses

            model_data = response.json()
            if "model" not in model_data:
                raise ValueError("Invalid model data format from trainer.")

            predictor.load_model(model_data["model"])
            cache.clear()
            print("Model loaded successfully.", flush=True)
            return model_data.get("evaluation")

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Failed to fetch model: {e}", flush=True)
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...", flush=True)
                time.sleep(retry_delay)
            else:
                print("Could not fetch model from trainer after several retries.", flush=True)
                return None


@app.on_event("startup")
def startup_event():
    """On startup, trigger the initial model training and loading."""
    print("Application startup: Initializing model...", flush=True)
    fetch_and_load_model()


@app.post("/reload")
def reload_model_endpoint():
    """An endpoint to manually trigger model retraining and reloading."""
    print("Manual model reload triggered...", flush=True)
    evaluation = fetch_and_load_model()
    if evaluation:
        return {"message": "Model reloaded successfully", "new_model_evaluation": evaluation}
    else:
        raise HTTPException(status_code=500, detail="Failed to reload model from trainer.")


@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        if predictor.model is None:
            raise ValueError(
                "Model is not loaded. Please load a model via the /reload endpoint or restart the service.")

        cached_prediction = cache.get(request.features)
        if cached_prediction:
            return {"prediction": cached_prediction, "source": "cache"}

        prediction = predictor.predict(request.features)
        cache.set(request.features, prediction)
        return {"prediction": prediction, "source": "model"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"An unexpected error occurred during prediction: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")