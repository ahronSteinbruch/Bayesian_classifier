import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class DataFrameRequest(BaseModel):
    data: str


@app.get("/")
def index():
    return {"status": "OK"}

