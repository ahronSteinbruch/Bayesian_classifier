# data_parser.py

import pandas as pd
from typing import Optional, List, Dict, Union
from fastapi import HTTPException
from pydantic import BaseModel
import json

class ModelData(BaseModel):
    data: List[Dict[str, Union[str, int, float]]]
async def parse_data(
    file_bytes: Optional[bytes],
    filename: Optional[str],
    csv_text: Optional[str],
    json_text: Optional[str],
    json_body: Optional[ModelData],  #👈 כאן - מקבלים את ModelData ולא רשימה פשוטה
):
    print(json_body)
    if file_bytes and filename:
        try:
            decoded = file_bytes.decode("utf-8")
            if filename.endswith(".csv"):
                return pd.read_csv(pd.io.common.StringIO(decoded))
            elif filename.endswith((".json", ".txt")):
                return pd.read_json(pd.io.common.StringIO(decoded), orient="records")
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    elif csv_text:
        return pd.read_csv(pd.io.common.StringIO(csv_text))

    elif json_text:
        try:
            return pd.DataFrame(json.loads(json_text))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON text: {str(e)}")

    elif json_body:
        return pd.DataFrame(json_body)  # 👈👈 ניגשים דרך json_body.data

    else:
        raise HTTPException(status_code=400, detail="No data provided")