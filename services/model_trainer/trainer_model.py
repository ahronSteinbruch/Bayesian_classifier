from pprint import pprint

class Trainer_model:
    def __init__(self, df):
        self.df = df
        self.target_values = df["target"].unique().tolist()


    def getWeights(self):
        weights = dict()
        targetsSize = dict()
        sizeOfModel = self.df.shape[0]

        for target in self.target_values:
            weights[target] = dict()
            target_df = self.df[self.df["target"] == target]  # Filter for current target
            targetsSize[target] = target_df.shape[0]/sizeOfModel
            for col in self.df.columns.tolist()[1:]:  # Skip the last column (assumed to be 'accepted')
                weights[target][col] = dict()
                num_values = self.df[col].unique().shape[0]
                sizeOfTarget = target_df.shape[0]
                ifZero = False
                for val in self.df[col].unique():
                    val_str = str(val)
                    # Count how many times this value appears in column for this target class
                    count = target_df[target_df[col] == val].shape[0]
                    weights[target][col][val_str] = count
                    if count == 0:
                        ifZero = True
                        weights[target][col][val_str] = 1
                for val in self.df[col].unique():
                    val_str = str(val)
                    if ifZero:
                        weights[target][col][val_str] = (weights[target][col][val_str]+1) / (num_values + sizeOfTarget)
                    else:
                        weights[target][col][val_str] = weights[target][col][val_str] / sizeOfTarget
        return weights, targetsSize
