import pandas as pd
from typing import Dict, Any

class ModelTrainer:
    def train(self, train_df: pd.DataFrame) -> Dict[str, Any]:
        print("Training model...", flush=True)
        target_values = train_df["target"].unique().tolist()
        weights = {}
        targets_size = {}
        model_size = len(train_df)

        for target in target_values:
            weights[target] = {}
            target_df = train_df[train_df["target"] == target]
            targets_size[target] = len(target_df) / model_size
            for col in train_df.columns[1:]:
                weights[target][col] = {}
                num_unique_vals = train_df[col].nunique()
                target_size = len(target_df)
                for val in train_df[col].unique():
                    count = len(target_df[target_df[col] == val])
                    weights[target][col][str(val)] = (count + 1) / (target_size + num_unique_vals)
        return {"weights": weights, "group_size": targets_size}