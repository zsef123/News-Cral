from src.newspapers.Donga import Donga
from  utils.SaveToFile import ArticleSave

if __name__=="__main__":
    newsClass = Donga("호스피스", "20000101","20170101")
    saver = ArticleSave("C:\\py\\test", 'Donga')
    print(newsClass.getQuery())
    pageCount = newsClass.getPageCount()
    for pageNumber in range(1, pageCount+1):
        pageUrls = newsClass.getPageHrefs( pageNumber )
        for pageUrl in pageUrls:
            datas= newsClass.getPage(pageUrl)
            saver.saveToTxt(datas)
    saver.txtMergeToExcel("testExcel")