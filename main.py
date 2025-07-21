import time
from pprint import pprint

import pandas as pd
import requests

# Give the services a moment to start up within the Docker network
print("Orchestrator is waiting for services to start...")
time.sleep(5)
print("Starting orchestration.")

# Load and prepare the data locally first
df = pd.read_csv("Intelligence_Selection.csv")
df = df.dropna()
# --- 1. Clean the Data ---
# URL now uses the service name 'cleaner' from docker-compose.yml
print("Step 1: Cleaning data...")
Cleaner_url = "http://cleaner:8001/clean_data"
clean_payload = {"df": df.to_dict(orient="records"), "colTargetName": "accepted"}
res = requests.post(Cleaner_url, json=clean_payload)
res.raise_for_status()
cleaned_df = pd.DataFrame(res.json())
print("Data cleaned successfully.")
print("-" * 30)

# --- 2. Split Data ---
print("Step 2: Splitting data (70% train, 30% test)...")
cleaned_df = cleaned_df.sample(frac=1, random_state=42).reset_index(drop=True)
test_size = int(len(cleaned_df) * 0.3)
test_df = cleaned_df.iloc[:test_size]
train_df = cleaned_df.iloc[test_size:]
print(f"Training set size: {len(train_df)}")
print(f"Testing set size: {len(test_df)}")
print("-" * 30)

# --- 3. Train the Model ---
# URL now uses the service name 'trainer'
print("Step 3: Training model...")
Trainer_url = "http://trainer:8002/train_model"
res = requests.post(Trainer_url, json={"df": train_df.to_dict(orient="records")})
res.raise_for_status()
model_parts = res.json()
model = {"weights": model_parts[0], "group_size": model_parts[1]}
print("Model trained successfully.")
print("-" * 30)

# --- 4. Load the Model into the Predictor ---
# URL now uses the service name 'predictor'
print("Step 4: Loading model into predictor...")
load_model_url = "http://predictor:8003/load_model"
res = requests.post(load_model_url, json=model)
res.raise_for_status()
print("Predictor response:", res.json())
print("-" * 30)

# --- 5. Evaluate the Model ---
# URLs use the service names 'evaluator' and 'predictor'
print("Step 5: Evaluating model performance...")
Evaluator_url = "http://evaluator:8004/evaluate"
Predict_url = (
    "http://predictor:8003/predict"  # The evaluator needs to know the predictor's URL
)

eval_payload = {"df": test_df.to_dict(orient="records"), "predictor_url": Predict_url}

res = requests.post(Evaluator_url, json=eval_payload)
res.raise_for_status()
print("\n--- Model Evaluation Report ---")
pprint(res.json())
print("-----------------------------")
