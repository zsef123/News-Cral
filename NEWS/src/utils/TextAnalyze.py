from collections import Counter
import pandas as pd

class MorphsCounter():
    def saveToExcel(self, counter):
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        df.rename(columns={'index':'morph', '0':'count'})
        df.to_excel(self.destFileDir, index=False, merge_cells=False)
        return

    def getMorphCounter(self, row):
        counter = Counter()
        for i,r in enumerate(row):
            morphs = self.analyer(r.strip())
            counter += Counter(morphs)
        return counter

    def __init__(self, sourceFileDir, destFileDir, analyzer = None):
        self.destFileDir = destFileDir
        xlsx = pd.ExcelFile(sourceFileDir) # 다중 시트는
        self.df = xlsx.parse(xlsx.sheet_names[0], index_col=None, convert_float=False,converters={'ID':str,'DATE':str})
        self.analyzer = analyzer
        return
class Corelation():
    def __init__(self, sourceFileDir, destFileDir):
        destXlsx = pd.ExcelFile(destFileDir)
        self.destDf = xlsx.parse(xlsx.sheet_names[0], index_col=None, convert_float=False)
        
        xlsx = pd.ExcelFile(sourceFileDir)
        self.sourDf = xlsx.parse(xlsx.sheet_names[0], index_col=None, convert_float=False)
        return