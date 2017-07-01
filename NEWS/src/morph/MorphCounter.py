from collections import Counter
import pandas as pd

class MorphCounter():
    def saveToExcel(self, counter):
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        df.rename(columns={'index':'morph', '0':'count'})
        df.to_excel(self.destFileDir+"morph.xlsx", index=False, merge_cells=False)
        return

    def getMorphCounter(self, rows):
        counter = Counter()
        for i, r in enumerate(rows):
            morphs = self.analyzer(r.strip())
            counter += Counter(morphs)
        return counter

    def __init__(self, sourceFileDir, destFileDir, analyzer = None):
        self.destFileDir = destFileDir
        xlsx = pd.ExcelFile(sourceFileDir)
        self.df = xlsx.parse(xlsx.sheet_names[0], index_col=None, convert_float=False,converters={'ID':str,'DATE':str})
        self.analyzer = analyzer
        return
