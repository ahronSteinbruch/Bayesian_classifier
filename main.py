import pandas as pd
def getData(path):
    df = pd.read_csv(path)
    return df

cleanData = getData("Intelligence_Selection.csv").dropna()



