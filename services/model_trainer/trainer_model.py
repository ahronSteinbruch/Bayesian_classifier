# services/model_trainer/trainer_model.py

from pprint import pprint


class Trainer_model:
    def __init__(self, df):
        self.df = df
        self.target_values = df["target"].unique().tolist()

    def getWeights(self):
        """
        Calculates the conditional probabilities for each feature value given a class (target),
        and the prior probability of each class. Uses Laplace (add-1) smoothing to handle
        zero-frequency events.
        """
        weights = {}
        targets_priors = {}
        total_rows = len(self.df)

        # Iterate over each possible target class ('Yes', 'No')
        for target in self.target_values:
            weights[target] = {}
            target_df = self.df[self.df["target"] == target]
            num_target_rows = len(target_df)

            # Calculate the prior probability of the target class
            targets_priors[target] = num_target_rows / total_rows

            # Iterate over each feature column (e.g., 'math_score', 'logic_score')
            for col in self.df.columns.tolist():
                if col == "target":
                    continue

                weights[target][col] = {}

                # Get the number of unique values for this feature in the whole dataset
                num_unique_values_in_col = self.df[col].nunique()

                # Calculate probabilities for each unique value in the feature column
                for unique_val in self.df[col].unique():
                    val_str = str(unique_val)

                    # Count occurrences of the value in rows with the current target
                    count = target_df[target_df[col] == unique_val].shape[0]

                    # Apply Laplace (add-1) smoothing
                    # P(value|target) = (count(value, target) + 1) / (count(target) + k)
                    # k is the number of unique values for the feature
                    smoothed_prob = (count + 1) / (
                        num_target_rows + num_unique_values_in_col
                    )
                    weights[target][col][val_str] = smoothed_prob

        pprint(weights)
        pprint(targets_priors)
        return weights, targets_priors
