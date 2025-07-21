from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

from .cache_service import Cache

app = FastAPI()
cache = Cache.get_instance()


class PredictGetRequest(BaseModel):
    features: Dict[str, Any]


class PredictPostRequest(BaseModel):
    features: Dict[str, Any]
    prediction: str


@app.get("/")
def index():
    return {"status": "Server running"}


@app.get("/predict")
def get_prediction_from_cache(req: PredictGetRequest, response: Response):
    # השתמש במודל Pydantic כדי לוודא את מבנה הקלט
    prediction = cache.try_predict(req.features)
    if prediction:
        return {"prediction": prediction}

    # אם אין תוצאה, החזר 404
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"detail": "Prediction not found in cache"}


@app.post("/predict")
def add_prediction_to_cache(req: PredictPostRequest):
    # תקן את שם המתודה
    cache.add_to_cache(req.features, req.prediction)
    return {"status": "Prediction added to cache"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
