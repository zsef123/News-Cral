import pandas as pd

class Corelation():
    def __init__(self, sourceFileDir, destFileDir):
        destXlsx = pd.ExcelFile(destFileDir)
        self.destDf = xlsx.parse(xlsx.sheet_names[0], index_col=None, convert_float=False)
        
        xlsx = pd.ExcelFile(sourceFileDir)
        self.sourDf = xlsx.parse(xlsx.sheet_names[0], index_col=None, convert_float=False)
        return
