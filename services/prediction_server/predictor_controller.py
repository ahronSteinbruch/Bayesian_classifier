from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .predictor_service import Predictor

app = FastAPI()


class ModelData(BaseModel):
    weights: Dict[str, Dict[str, Dict[str, float]]]
    group_size: Dict[str, float]


class PredictRequest(BaseModel):
    features: Dict[str, Any]


@app.get("/")
def index():
    return {"status": "Server running"}


@app.post("/load_model")
def load_model(model_data: ModelData):
    global predictor
    predictor = Predictor(model_data.weights, model_data.group_size)
    return {"status": "Model loaded"}




@app.post("/predict")
def predict(req: PredictRequest):
    if predictor is None:
        raise HTTPException(status_code=400, detail="Model not loaded yet")

    cache_response = predictor.search_in_cache(req.features)
    if cache_response.status_code == 200:
        # חלץ את התחזית מתוך ה-JSON שהתקבל
        prediction = cache_response.json().get("prediction")
        print("Prediction found in cache.")
        return {"prediction": prediction}
    print("Prediction not in cache. Calculating...")
    prediction = predictor.predict(req.features)
    predictor.save_prediction_in_cache(req.features, prediction)

    return {"prediction": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8003)
