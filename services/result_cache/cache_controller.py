from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .cache_service import Cache

app = FastAPI()
cache = Cache.get_instance()
class PredictRequest(BaseModel):
    features: Dict[str, Any]

class InsertNewPredict(BaseModel):
    features: Dict[str, Any]
    prediction: str

@app.get("/")
def index():
    return {"status": "Server running"}


@app.get("/predict")
def predict(req: PredictRequest):
    return cache.try_predict(req.features)

app.post("/new_predict")
def add_predict(req: InsertNewPredict):
    return cache.add_predict(req.features , req.prediction)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8005)
