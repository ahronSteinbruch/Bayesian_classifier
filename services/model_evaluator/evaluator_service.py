from services.prediction_server.predictor_service import Predictor

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
from typing import Dict


class Evaluator:
    def __init__(self, df: pd.DataFrame, predictor):
        """
        Args:
            df (pd.DataFrame): טבלת בדיקה הכוללת עמודת 'target'
            predictor (Predictor): מופע של המחלקה Predictor
        """
        self.df = df
        self.predictor = predictor

    def _calculate_metrics(self, y_true, y_pred) -> Dict[str, float]:
        """חישוב דיוק, precision ו-recall עם ממוצע משוקלל"""
        return {
            "accuracy": round(accuracy_score(y_true, y_pred), 2),
            "precision": round(precision_score(y_true, y_pred, average='weighted', zero_division=0), 2),
            "recall": round(recall_score(y_true, y_pred, average='weighted', zero_division=0), 2),
        }

    def evaluate(self) -> Dict[str, float]:
        """
        מריץ חיזוי על כל שורה ובודק ביצועי המודל.
        """
        X = self.df.drop(columns=["target"])
        y_true = self.df["target"].tolist()
        y_pred = []

        print(f"Starting evaluation... Evaluating {len(X)} rows using local Predictor.")

        for _, row in X.iterrows():
            payload = row.to_dict()
            try:
                prediction = self.predictor.predict(payload)
                y_pred.append(prediction)
            except Exception as e:
                print(f"Prediction error for row {payload}: {e}")
                y_pred.append(None)

        # סינון שורות שנכשלו
        valid_predictions = [(true, pred) for true, pred in zip(y_true, y_pred) if pred is not None]
        if not valid_predictions:
            return {"error": "No valid predictions."}

        y_true_filtered, y_pred_filtered = zip(*valid_predictions)
        print("Evaluation complete. Calculating metrics.")
        return self._calculate_metrics(y_true_filtered, y_pred_filtered)

