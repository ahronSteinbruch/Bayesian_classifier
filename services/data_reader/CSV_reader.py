import pandas as pd
class CsvReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        try:
            df = pd.read_csv(self.file_path)
            return df
        except Exception as e:
            print(e)