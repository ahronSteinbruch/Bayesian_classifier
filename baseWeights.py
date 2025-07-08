from pprint import pprint


class BaseWeights:
    def __init__(self, df):
        self.df = df
        self.target_values = df["accepted"].unique()

    def getWeights(self):
        weights = dict()

        for target in self.target_values:
            weights[target] = dict()
            target_df = self.df[self.df["accepted"] == target]  # Filter for current target

            for col in self.df.columns.tolist()[:-1]:  # Skip the last column (assumed to be 'accepted')
                weights[target][col] = dict()
                num_values = self.df[col].unique().shape[0]
                ifZero = 0
                for val in self.df[col].unique():
                    val_str = str(val)
                    # Count how many times this value appears in column for this target class
                    count = target_df[target_df[col] == val].shape[0]
                    weights[target][col][val_str] = count
                    if count == 0:
                        ifZero = num_values
                        weights[target][col][val_str] = 1
                for val in self.df[col].unique():
                    val_str = str(val)
                    weights[target][col][val_str] = weights[target][col][val_str] / (num_values + ifZero)

        pprint(weights)
        return weights
