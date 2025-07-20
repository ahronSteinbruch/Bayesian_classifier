# import pandas as pd
# import requests
# from pprint import pprint
#
# # Load and prepare the data locally first
# df = pd.read_csv('Intelligence_Selection.csv')
# df = df.dropna()
# # --- 1. Clean the Data ---
# # Call the cleaner service to drop nulls and format the target column
# print("Step 1: Cleaning data...")
# Cleaner_url = 'http://127.0.0.1:8001/clean_data'
# clean_payload = {"df": df.to_dict(orient="records"), "colTargetName": "accepted"}
# res = requests.post(Cleaner_url, json=clean_payload)
# res.raise_for_status() # Raise an exception for bad status codes
# cleaned_df = pd.DataFrame(res.json())
# print("Data cleaned successfully.")
# pprint(cleaned_df.head())
# print("-" * 30)
#
# # --- 2. Train the Model ---
# # Send the cleaned data to the trainer service
# print("Step 2: Training model...")
# Trainer_url = 'http://127.0.0.1:8002/train_model'
# res = requests.post(Trainer_url, json={"df": cleaned_df.to_dict(orient="records")})
# res.raise_for_status()
# model_parts = res.json()
#
# # Structure the model correctly for the prediction server
# model = {"weights": model_parts[0], "group_size": model_parts[1]}
# print("Model trained successfully.")
# # pprint(model)
# print("-" * 30)
#
# # --- 3. Load the Model into the Predictor ---
# # Send the trained model to the predictor's /load_model endpoint
# print("Step 3: Loading model into predictor...")
# load_model_url = 'http://127.0.0.1:8003/load_model'
# res = requests.post(load_model_url, json=model)
# res.raise_for_status()
# print("Predictor response:", res.json())
# print("-" * 30)
#
# # --- 4. Make a Prediction ---
# # Now, send a prediction request to the /predict endpoint
# print("Step 4: Making a prediction...")
# predict_url = 'http://127.0.0.1:8003/predict'
#
# # Create a sample payload from the first row of your cleaned data (excluding the target)
# sample_features = cleaned_df.drop(columns=['target']).iloc[0].to_dict()
#
# prediction_payload = {"features": sample_features}
# print("Sending features for prediction:")
# pprint(prediction_payload)
#
# res = requests.post(predict_url, json=prediction_payload)
# res.raise_for_status()
# print("\nPrediction result:")
# pprint(res.json())

# main.py

import pandas as pd
import requests
from pprint import pprint
import numpy as np

# Load and prepare the data locally first
df = pd.read_csv('Intelligence_Selection.csv')
df = df.dropna()
# --- 1. Clean the Data ---
print("Step 1: Cleaning data...")
Cleaner_url = 'http://127.0.0.1:8001/clean_data'
clean_payload = {"df": df.to_dict(orient="records"), "colTargetName": "accepted"}
res = requests.post(Cleaner_url, json=clean_payload)
res.raise_for_status()
cleaned_df = pd.DataFrame(res.json())
print("Data cleaned successfully.")
print("-" * 30)

# --- 2. Split Data into Training and Testing Sets ---
print("Step 2: Splitting data (70% train, 30% test)...")
# Shuffle the DataFrame to ensure random splitting
cleaned_df = cleaned_df.sample(frac=1, random_state=42).reset_index(drop=True)
test_size = int(len(cleaned_df) * 0.3)
test_df = cleaned_df.iloc[:test_size]
train_df = cleaned_df.iloc[test_size:]
print(f"Training set size: {len(train_df)}")
print(f"Testing set size: {len(test_df)}")
print("-" * 30)


# --- 3. Train the Model on the Training Set ---
print("Step 3: Training model...")
Trainer_url = 'http://127.0.0.1:8002/train_model'
res = requests.post(Trainer_url, json={"df": train_df.to_dict(orient="records")})
res.raise_for_status()
model_parts = res.json()
model = {"weights": model_parts[0], "group_size": model_parts[1]}
print("Model trained successfully.")
print("-" * 30)

# --- 4. Load the Model into the Predictor ---
print("Step 4: Loading model into predictor...")
load_model_url = 'http://127.0.0.1:8003/load_model'
res = requests.post(load_model_url, json=model)
res.raise_for_status()
print("Predictor response:", res.json())
print("-" * 30)

# --- 5. Evaluate the Model with the Test Set ---
print("Step 5: Evaluating model performance...")
Evaluator_url = 'http://127.0.0.1:8004/evaluate'
Predict_url = 'http://127.0.0.1:8003/predict'

eval_payload = {
    "df": test_df.to_dict(orient="records"),
    "predictor_url": Predict_url
}

res = requests.post(Evaluator_url, json=eval_payload)
res.raise_for_status()
print("\n--- Model Evaluation Report ---")
pprint(res.json())
print("-----------------------------")