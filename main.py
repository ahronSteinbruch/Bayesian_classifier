import pandas as pd
from services.model_trainer.trainer_model import Trainer_model


def getData(path):
    df = pd.read_csv(path)
    return df

cleanData = getData("Intelligence_Selection.csv").dropna()

data = Trainer_model(cleanData)
data.getWeights()

