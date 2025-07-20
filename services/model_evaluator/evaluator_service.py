import pandas as pd
import requests
from sklearn.metrics import accuracy_score, precision_score, recall_score
from typing import Dict


class Evaluator:

    @staticmethod
    def _calculate_metrics(y_true, y_pred) -> Dict[str, float]:
        """Calculates accuracy, precision, and recall."""
        return {
            "accuracy": round(accuracy_score(y_true, y_pred), 2),
            "precision": round(precision_score(y_true, y_pred, average='weighted', zero_division=0), 2),
            "recall": round(recall_score(y_true, y_pred, average='weighted', zero_division=0), 2),
        }

    @staticmethod
    def evaluate(df: pd.DataFrame, predictor_url: str) -> Dict[str, float]:
        """
        Evaluates the model by sending each row of the test data to the predictor service.

        Args:
            df (pd.DataFrame): The test dataframe containing features and a 'target' column.
            predictor_url (str): The URL of the '/predict' endpoint on the prediction server.

        Returns:
            Dict[str, float]: A dictionary containing the model's performance metrics.
        """
        X_test = df.drop(columns=["target"])
        y_true = df["target"].tolist()
        y_pred = []

        print(f"Starting evaluation... Sending {len(X_test)} rows to predictor at {predictor_url}")

        # Send each row to the predictor service for a prediction
        for _, row in X_test.iterrows():
            payload = {"features": row.to_dict()}
            try:
                response = requests.post(predictor_url, json=payload)
                response.raise_for_status()  # Raise an exception for bad status codes
                prediction = response.json().get("prediction")
                y_pred.append(prediction)
            except requests.exceptions.RequestException as e:
                print(f"Error calling predictor service for row {row.to_dict()}: {e}")
                # Add a placeholder or handle the error as appropriate
                y_pred.append(None)  # Or a default value

        # Filter out failed predictions if any
        valid_predictions = [(true, pred) for true, pred in zip(y_true, y_pred) if pred is not None]
        if not valid_predictions:
            return {"error": "Could not get any predictions from the server."}

        y_true_filtered, y_pred_filtered = zip(*valid_predictions)

        print("Evaluation complete. Calculating metrics.")
        return Evaluator._calculate_metrics(y_true_filtered, y_pred_filtered)
