from typing import Dict, List, Optional, Union

import pandas as pd
import uvicorn
from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from .data_parser import parse_data

app = FastAPI()


class ModelData(BaseModel):
    data: List[Dict[str, Union[str, int, float]]]


@app.get("/")
def index():
    return {"my name": "data reader", "status": "OK", "port": 8000}


@app.post("/parse_data")
def test(model_data: ModelData):
    df = pd.DataFrame(model_data.data)
    return df.to_dict(orient="records")


@app.get("/expected_schema")
def expected_schema():
    return {
        "message": "Generic Data Parser Service",
        "usage": {
            "POST /parse_data": "Send file, csv_text, json_text, or JSON body with records",
            "returns": "pandas dataframe",
        },
    }


@app.post("/parse_dataaaa")
async def upload_data(
    file: Optional[UploadFile] = File(None),
    csv_text: Optional[str] = Form(None),
    json_text: Optional[str] = Form(None),
    json_body: Optional[ModelData] = Body(None),  # כאן מקבלים את {"data": [...]}
):
    contents = None
    filename = None

    if file:
        contents = await file.read()
        filename = file.filename

    records = None
    if json_body:
        records = json_body.data  # 👈👈👈 ניגשים ל-mapped key 'data'
    print(records)
    df = await parse_data(contents, filename, csv_text, json_text, records)

    return {
        "message": "Data parsed successfully",
        "shape": df.shape,
        "columns": list(df.columns),
        "sample": df.head().to_dict(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
