import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from .trainer_model import Trainer_model
import pandas as pd

class JSONData(BaseModel):
    df: List[Dict[str, Union[str, int, float]]]

app = FastAPI()

@app.get('/')
def index():
    return \
        {
        'status': 'OK',
            'my name': 'model trainer',
            'port': 8002
        }

@app.post('/train_model')
async def clean_data(payload: JSONData):
    df = pd.DataFrame(payload.df)
    treiner = Trainer_model(df)
    return treiner.getWeights()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)

