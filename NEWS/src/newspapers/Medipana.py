from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import re
import math 

class Medipana(NewsCralwerInitializer, NewsCralwerGetUrl):
    """description of class"""
    def setQuery(self, query):
        return super().setQuery(query)
    def getQuery(self):
        return super().getQuery()
    def setDate(self, sDate, eDate): #yyyymmdd
        #기간검색 불가
        return
    def __init__(self):
        pass
    def __init__(self, query, sDate, eDate):
        return super().__init__(query,sDate, eDate)

    def getPageCount(self):
        page = '1'
        while 1:
            searchUrl = "http://www.medipana.com/news/news_list_new.asp?Page=" + page + "&MainKind=A&NewsKind=106&vCount=20&vKind=1&sID=&sWord=" + self.query + "&sDate="
            soup = Soup.requests(searchUrl, parser='html.parser')
            nextButton = soup.find('img', src='../images/paging_next.gif').parent
            if nextButton.name != 'a':
                lastLink = soup.find_all('td', align='center')[1].find_all('a')[-1]['href']
                page = re.sub("\D", "", lastLink)[:2]   
                break
            page = re.sub("\D", "", nextButton['href'])[:2]           
        return int(page)

    def getPageHrefs(self, count):
        searchUrl = "http://www.medipana.com/news/news_list_new.asp?Page=" + str(count) + "&MainKind=A&NewsKind=106&vCount=20&vKind=1&sID=&sWord=" + self.query + "&sDate="
        soup = Soup.requests(searchUrl, parser="html.parser")        
        searchBox = soup.find_all('a', class_='import_middle_title1')
        regex = re.compile("&sWord=(.*)")
        pageHrefs = ["http://www.medipana.com/" + regex.sub("", x.get('href')[2:]) for x in searchBox]
        return pageHrefs

    def getPage(self, url):
        soup = Soup.requests(url,parser='html.parser')
        articleID = re.search("NewsNum=[0-9]*",url).group()[8:]
        articleDate = re.sub("\D","",soup.find_all('a',class_='plan_1_1')[1].get_text())[:8]
        articleTitle = soup.find('div',class_='detailL').get_text().strip()

        bodyTag = soup.find('div',style="font:굴림; LINE-HEIGHT: 22px;letter-spacing:0px;text-align:justify; ")
        if bodyTag.find('div') is not None:
            articleTxtList = [div.get_text(separator="\n").strip() for div in bodyTag.find_all('div') ]
        else:
            adTags = bodyTag.find_all('table')
            for element in adTags:
                element.decompose()
            articleTxtList = []

        if len(articleTxtList) < 2:
            articleTxt = bodyTag.get_text(separator="\n\n").strip()
        else:
            articleTxt = "\n".join(articleTxtList)
        return (articleID, articleDate, articleTitle, articleTxt)

