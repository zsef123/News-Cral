import os
import re
import xlsxwriter

class ArticleSave(object):
    """description of class"""
    def sefFileDir(self, fileDir):
        self.fileDir = fileDir
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)            
        if not os.path.exists(fileDir + "\\texts"):
            os.makedirs(fileDir + "\\texts")
        return 1
    def __init__(self, fileDir, name):
        self.name = name
        self.sefFileDir(fileDir)
        return

    def saveToTxt(self, articleDatas):
        if len(articleDatas) != 4:
            raise AttributeError("articleDatas Length Check", articleDatas)
        articleID = articleDatas[0]
        articleDate = articleDatas[1]     
        articleTitle = articleDatas[2]
        articleTxt = articleDatas[3]
        with open(self.fileDir + "\\texts\\" + articleID + ".txt", 'w', encoding='utf-8') as article:            
            article.write("<date>\n" + articleDate + "\n</date>")
            article.write("<title>\n" + articleTitle + "\n</title>")
            article.write("<text>\n" + articleTxt + "\n</text>")
        return
    def loadTxt(self, articleFileName):
        with open(self.fileDir + "\\texts\\" + articleFileName, 'r', encoding='utf-8') as article:
            text = article.read()            
            articleDate = re.search("<date>[\w\W]*<\/date>", text).group()[7: -8]
            articleTitle = re.search("<title>[\w\W]*<\/title>", text).group()[8: -9]
            articleTxt = re.search("<text>[\w\W]*<\/text>", text).group()[7: -8]
        articleID = articleFileName[:-4]
        return (articleID, articleDate, articleTitle, articleTxt)
    def txtMergeToExcel(self, xlsxFileName):
        workbook = xlsxwriter.Workbook(self.fileDir+"\\"+ xlsxFileName + '.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'ID', bold)
        worksheet.write('B1', 'Date', bold)         
        worksheet.write('C1', 'Title', bold)         
        worksheet.write('D1', 'Text', bold)
        textFileList = [f for f in os.listdir(self.fileDir+"\\texts")]
        for row, textFile in enumerate(textFileList):
            articleDatas = self.loadTxt(textFile)
            for col, data in enumerate(articleDatas):
                worksheet.write(row+1, col, data)
        workbook.close()
        return