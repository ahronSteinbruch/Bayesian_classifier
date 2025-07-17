import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
import pandas as pd


app = FastAPI()
class DataFrameRequest(BaseModel):
    data: str

@app.get('/')
def index():
    return {'status': 'OK'}



