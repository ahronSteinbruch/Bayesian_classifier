import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from predictor import Predictor
from cache import Cache
import requests

app = FastAPI()
predictor = Predictor()
cache = Cache()


class PredictionRequest(BaseModel):
    features: Dict[str, Any]

def reload_model():
    print("Reloading model...", flush=True)
    response = requests.get("http://trainer:8080/reload_model")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to reload model")
    else:
        predictor.load_model(response.json())
@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        cached_prediction = cache.get(request.features)
        if cached_prediction:
            return {"prediction": cached_prediction, "source": "cache"}
        prediction = predictor.predict(request.features)
        cache.set(request.features, prediction)
        return {"prediction": prediction, "source": "model"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))