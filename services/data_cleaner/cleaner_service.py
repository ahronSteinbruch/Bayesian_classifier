class Cleaner:
    def __init__(self, df,colTargetName):
        self.df = df
        self.colTargetName = colTargetName
        self.cleanData()
        self.prepareData()

    def cleanData(self):
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()

    def prepareData(self):
        """
        take the target column and make it the first column
        rename the target column
        """
        self.df = self.df.rename(columns={self.colTargetName: "target"})
        self.df = self.df[["target"] + [col for col in self.df.columns if col != "target"]]

    def getData(self):
        return self.df