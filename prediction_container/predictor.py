from typing import Dict, Any
class Predictor:
    def __init__(self):
        self.model = None

    def load_model(self, model_data: Dict[str, Any]):
        self.model = model_data
    def predict(self, features: Dict[str, Any]) -> str:
        if not self.model:
            raise ValueError("Model is not loaded.")
        options = {}
        for option in self.model["weights"]:
            result = 1.0
            for feature, value in features.items():
                prob = self.model["weights"].get(option, {}).get(feature, {}).get(str(value), 1e-6)
                result *= prob
            result *= self.model["group_size"].get(option, 1e-6)
            options[option] = result
        return max(options, key=options.get)