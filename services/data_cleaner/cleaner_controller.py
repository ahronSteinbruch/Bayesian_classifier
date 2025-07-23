import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
import pandas as pd
from .cleaner_service import Cleaner

class JSONData(BaseModel):
    df: List[Dict[str, Union[str, int, float, None]]]
    colTargetName: str

app = FastAPI()

@app.get('/')
def index():
    return {'status': 'OK'}


@app.post('/clean_data')
async def clean_data(payload: JSONData):
    print(payload)
    df = pd.DataFrame(payload.df)
    colTargetName = payload.colTargetName
    print(colTargetName)
    df = Cleaner(df,colTargetName).getData()
    return df.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
