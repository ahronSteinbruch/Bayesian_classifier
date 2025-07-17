import pandas as pd
import requests
from pprint import pprint


df = pd.read_csv('Intelligence_Selection.csv')
df = df.dropna()

Reader_url = 'http://127.0.0.1:8000/parse_data'
res = requests.post(Reader_url, json={"data": df.to_dict(orient="records")})

Cleaner_url = 'http://127.0.0.1:8001/clean_data'
res = requests.post(Cleaner_url, json={"df":df.to_dict(orient="records") , "colTargetName": "accepted"})

cleaned_df = pd.DataFrame(res.json())
print(cleaned_df)
Trainer_url = 'http://127.0.0.1:8002/train_model'
res = requests.post(Trainer_url, json={"df":cleaned_df.to_dict(orient="records")})

model = res.json()
model = {"weights": model[0], "group_size": model[1]}
pprint(model)
model_url = 'http://127.0.0.1:8003/predict'
res = requests.post(model_url, json= model)
pprint(res.json())