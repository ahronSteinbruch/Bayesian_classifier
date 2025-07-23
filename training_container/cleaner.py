import pandas as pd
import numpy as np

class DataCleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        print("Cleaning data...", flush=True)
        df = df.replace(np.nan, None)
        df = df.dropna()
        df = df.drop_duplicates()
        df = df.rename(columns={"accepted": "target"})
        return df[["target"] + [col for col in df.columns if col != "target" and col != "accepted"]]