import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Union
import pandas as pd
from evaluator_service import Evaluator


# Pydantic model for the incoming request data
class EvaluationRequest(BaseModel):
    df: List[Dict[str, Union[str, int, float, None]]]
    predictor_url: str


app = FastAPI()


@app.get('/')
def index():
    return {
        'my name': 'model evaluator',
        'status': 'OK',
        'port': 8004
    }


@app.post('/evaluate')
async def evaluate_model(request: EvaluationRequest):
    """
    Receives test data and a predictor URL, and returns model performance metrics.
    """
    try:
        # Convert the incoming data to a DataFrame
        test_df = pd.DataFrame(request.df)

        # Call the static evaluation method from the service
        results = Evaluator.evaluate(test_df, request.predictor_url)

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8004)
