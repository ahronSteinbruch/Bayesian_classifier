import pandas as pd
import requests
import numpy as np
from pprint import pprint


class Orchestrator:
    def __init__(self):
        # Define URLs for internal services, all on localhost
        self.cleaner_url = "http://localhost:8001"
        self.trainer_url = "http://localhost:8002"
        self.predictor_url = "http://localhost:8003"
        self.evaluator_url = "http://localhost:8004"
        self.cache_url = "http://localhost:8005"

        # Run the full train-and-evaluate sequence upon initialization
        self.initialize_system_and_evaluate()

    def initialize_system_and_evaluate(self):
        """
        Coordinates data cleaning, splitting, model training, loading, and evaluation.
        """
        print("--- Orchestrator: Starting Full Train & Evaluate Sequence ---")

        # --- Step 1: Load and Clean the Full Dataset ---
        print("\n--- Step 1: Loading and Cleaning Data ---")
        df = pd.read_csv('Intelligence_Selection.csv')
        df = df.replace(np.nan, None)  # Handle NaN for JSON compatibility

        clean_payload = {"df": df.to_dict(orient="records"), "colTargetName": "accepted"}
        res = requests.post(f"{self.cleaner_url}/clean_data", json=clean_payload)
        res.raise_for_status()
        cleaned_df = pd.DataFrame(res.json())
        print("Data cleaned successfully.")

        # --- Step 2: Split Data into Training and Testing Sets ---
        print("\n--- Step 2: Splitting data (70% train, 30% test) ---")
        # Shuffle the DataFrame to ensure random splitting
        cleaned_df = cleaned_df.sample(frac=1, random_state=42).reset_index(drop=True)
        train_size = int(len(cleaned_df) * 0.7)
        train_df = cleaned_df.iloc[:train_size]
        test_df = cleaned_df.iloc[train_size:]
        print(f"Total records: {len(cleaned_df)}")
        print(f"Training set size: {len(train_df)}")
        print(f"Testing set size: {len(test_df)}")

        # --- Step 3: Train the Model on the Training Set ---
        print("\n--- Step 3: Training model on 70% of the data ---")
        res = requests.post(f"{self.trainer_url}/train_model", json={"df": train_df.to_dict(orient="records")})
        res.raise_for_status()
        model_parts = res.json()
        model = {"weights": model_parts[0], "group_size": model_parts[1]}
        print("Model trained successfully.")

        # --- Step 4: Load the Model into the Predictor ---
        print("\n--- Step 4: Loading model into predictor ---")
        load_model_url = f"{self.predictor_url}/load_model"
        res = requests.post(load_model_url, json=model)
        res.raise_for_status()
        print(f"Predictor response: {res.json()}")

        # --- Step 5: Evaluate the Model with the Test Set ---
        print("\n--- Step 5: Evaluating model performance with the remaining 30% ---")
        # The URL for the predictor's predict endpoint, as needed by the evaluator
        predictor_predict_url = f"{self.predictor_url}/predict"

        eval_payload = {
            "df": test_df.to_dict(orient="records"),
            "predictor_url": predictor_predict_url
        }

        res = requests.post(f"{self.evaluator_url}/evaluate", json=eval_payload)
        res.raise_for_status()

        print("\n--- MODEL EVALUATION REPORT ---")
        pprint(res.json())
        print("---------------------------------")

        print("\n--- Orchestrator: System is ready for predictions via the /classify endpoint. ---")

    def predict_case(self, features: dict) -> str:
        """
        Gets a prediction for a single case, using the cache first.
        (This function remains unchanged)
        """
        # 1. Try cache
        try:
            cache_res = requests.get(f"{self.cache_url}/predict", json={"features": features})
            if cache_res.status_code == 200:
                print("Prediction found in cache.")
                return cache_res.json().get("prediction")
        except requests.exceptions.RequestException as e:
            print(f"Could not reach cache service: {e}")

        # 2. Call predictor
        print("Prediction not in cache, calling predictor service...")
        predict_payload = {"features": features}
        res = requests.post(f"{self.predictor_url}/predict", json=predict_payload)
        res.raise_for_status()
        prediction = res.json().get("prediction")

        # 3. Add to cache
        try:
            cache_payload = {"features": features, "prediction": prediction}
            requests.post(f"{self.cache_url}/predict", json=cache_payload)
            print("Prediction added to cache.")
        except requests.exceptions.RequestException as e:
            print(f"Could not update cache service: {e}")

        return prediction