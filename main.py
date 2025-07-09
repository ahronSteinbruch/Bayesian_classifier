import pandas as pd
from services.model_trainer.trainer_model import Trainer_model
from services.data_reader.CSV_reader import CsvReader
from services.data_cleaner.cleaner_service import Cleaner
def getData(path):
    df = CsvReader(path).read_data()
    return df

path = 'Intelligence_Selection.csv'
df = getData(path)
targetColumnName = "accepted"
cleanData = Cleaner(df, targetColumnName).getData()

data = Trainer_model(cleanData)
data.getWeights()

