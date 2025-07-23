# services/orchestrator/orchestrator_controller.py
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from .orchestrator_service import Orchestrator

app = FastAPI()

# Initialize the orchestrator service, which will trigger the training process
# This happens only once when the application starts
orchestrator = Orchestrator()

class ClassificationRequest(BaseModel):
    features: Dict[str, Any]

@app.get('/')
def index():
    return {'status': 'Orchestrator is running and model is loaded.'}

@app.post('/classify')
async def classify_case(request: ClassificationRequest):
    """
    Receives a single case and returns a classification.
    """
    try:
        prediction = orchestrator.predict_case(request.features)
        return {"classification_result": prediction}
    except Exception as e:
        # If any step in the prediction process fails, return an error
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # The main entry point to run the entire system
    uvicorn.run(app, host="127.0.0.1", port=80)



