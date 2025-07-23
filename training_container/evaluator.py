import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
from typing import Dict, Any

class ModelEvaluator:
    def _predict_internally(self, model: Dict[str, Any], features: Dict[str, Any]) -> str:
        options = {}
        for option in model["weights"]:
            result = 1.0
            for feature, value in features.items():
                prob = model["weights"].get(option, {}).get(feature, {}).get(str(value), 1e-6)
                result *= prob
            result *= model["group_size"].get(option, 1e-6)
            options[option] = result
        return max(options, key=options.get)

    def evaluate(self, model: Dict[str, Any], test_df: pd.DataFrame) -> Dict[str, float]:
        print("Evaluating model...", flush=True)
        y_true = test_df["target"].tolist()
        X_test = test_df.drop(columns=["target"])
        y_pred = [self._predict_internally(model, row.to_dict()) for _, row in X_test.iterrows()]
        return {
            "accuracy": round(accuracy_score(y_true, y_pred), 3),
            "precision": round(precision_score(y_true, y_pred, average='weighted', zero_division=0), 3),
            "recall": round(recall_score(y_true, y_pred, average='weighted', zero_division=0), 3),
        }