from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import math
import re

class Medicaltimes(NewsCralwerInitializer, NewsCralwerGetUrl):
    """description of class"""
    def setQuery(self, query):
        return super().setQuery(query)
    def getQuery(self):
        return super().getQuery()
    def setDate(self, sDate, eDate): #yyyymmdd
        self.startDate = sDate 
        self.endDate = eDate 
    def __init__(self):
        pass
    def __init__(self, query, sDate, eDate):
        return super().__init__(query,sDate, eDate)

    def getPageCount(self):
        searchUrl = "http://www.medicaltimes.com/Users4/Search/searchEach.html?nStart=1&KeyWord="+self.query+"&searchType=news"
        soup = Soup.requests(searchUrl,parser='html.parser')

        try:
            maxPageCnt=soup.find_all('tr',height='40')[0].contents[1].contents[-1].get('href')
        except AttributeError:
            maxPageCnt=soup.find_all('tr',height='40')[0].find_all('a')[-1].get('href')
        maxPageTag = soup.find_all('img', src="http://image.medicaltimes.com/common/1_57.jpg")[0].parent
        pageCount=int(re.search("nStart=[0-9]*",maxPageTag['href']).group()[7:])
        return math.floor(pageCount/10)

    def getPageHrefs(self, count):
        count = (count-1)*10
        searchUrl= "http://www.medicaltimes.com/Users4/Search/searchEach.html?nStart="+str(count)+"&KeyWord="+self.query+"&searchType=news"
        soup = Soup.requests(searchUrl,parser='html.parser')
        searchBox=soup.find('table', class_="news_view_contents").find_all('a', style="font-size:11pt; color:darkblue")
        regex= re.compile("&nSection=(.*)")
        pageHrefs=[regex.sub("",x.get('href')) for x in searchBox]
        return pageHrefs

    def getPage(self, url):
        soup = Soup.requests(url, parser='html.parser', encoding="euc-kr")
        if not soup.find('body'):
            print("Error url : %s"%(url))
            return (0, "error", "error", 0)

        articleID=re.search("ID=[0-9]*",url).group()[3:]
        articleTitle=soup.find('td',class_='px21 bk fbd lh15 lt').get_text().strip()
        articleDate=re.sub("\D","",soup.select("#html_head > table:nth-of-type(2) > tr:nth-of-type(2) > td:nth-of-type(1) > table > tr > td > div > table:nth-of-type(1) > tr:nth-of-type(6) > td > font")[0].get_text())[:8]

        photoCaption = soup.find('td', id='NEWS_CONTENT').find_all('table')
        for element in photoCaption:
            element.decompose()
        articleTxt=soup.find('td', id='NEWS_CONTENT').get_text(separator="\n").strip()
        return (articleID, articleDate, articleTitle, articleTxt)

