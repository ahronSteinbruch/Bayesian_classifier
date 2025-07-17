import requests
from services.prediction_server.predictor_service import Predictor
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import accuracy_score, precision_score, recall_score

class Evaluator:
    def __init__(self, df, predictor: Predictor):
        self.df = df
        self.predictor = predictor

    def evaluate(self):
        X = self.df.drop(columns=["target"])
        y_true = self.df["target"]

        y_pred = []
        for _, row in X.iterrows():
            payload = row.to_dict()
            prediction = self.predictor.predict(payload)
            y_pred.append(prediction)

        return self._calculate_metrics(y_true, y_pred)

    def _calculate_metrics(self, y_true, y_pred):
        return {
            "accuracy": round(accuracy_score(y_true, y_pred), 2),
            "precision": round(precision_score(y_true, y_pred, zero_division=0), 2),
            "recall": round(recall_score(y_true, y_pred, zero_division=0), 2),
        }
