from typing import Dict
import requests

class Predictor:
    def __init__(
        self,
        model_weights: Dict[str, Dict[str, Dict[str, float]]],
        targets_size: Dict[str, float],
    ):
        self.model_weights = model_weights
        self.targets_size = targets_size
    def predict(self, row: dict) -> str:
        options = {}
        for option in self.model_weights:
            options[option] = self.calculate_probabilities(row, option)
        return max(options, key=options.get)

    def calculate_probabilities(self, row: dict, option: str) -> float:
        result = 1.0
        for feature, value in row.items():
            prob = (
                self.model_weights.get(option, {})
                .get(feature, {})
                .get(str(value), 1e-6)
            )
            result *= prob
        result *= self.targets_size.get(option, 1e-6)
        return result

    def search_in_cech(self, row: dict):
        res = requests.get("http://cesh:8005/predict", json=row)
        return res
    def save_prediction_in_cache(self, row: dict, prediction: str):
        requests.post("http://cache:8005/predict", json={"features": row, "prediction": prediction})