from ..NewsCralwer import NewsCralwerInitializer
from ..NewsCralwer import NewsCralwerGetUrl
from ..Soup import Soup
import math
import re

class Dailymedi(NewsCralwerInitializer, NewsCralwerGetUrl):
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
        searchUrl="http://dailymedi.com/search.php?pg=1&search_word="+self.query+"&search_jogun=1&start_date="+self.startDate+"&end_date="+self.endDate+"&file=search1.html&numberpart=&category_select=22&numberpart=&thread=&pick=&file2=&file=search1.html&area=&&user_id=&&user_name=&&start_date="+self.startDate+"&end_date="+self.endDate
        soup = Soup.requests(searchUrl)
        return math.floor(int(soup.find('span',class_='news_count').get_text())/30)

    def getPageHrefs(self, count):
        searchUrl="http://dailymedi.com/search.php?pg="+str(count)+"&search_word="+self.query+"&search_jogun=1&start_date="+self.startDate+"&end_date="+self.endDate+"&file=search1.html&numberpart=&category_select=22&numberpart=&thread=&pick=&file2=&file=search1.html&area=&&user_id=&&user_name=&&start_date="+self.startDate+"&end_date="+self.endDate
        soup = Soup.requests(searchUrl)
        pageHrefTags=soup.find_all('a',class_='smfont7')
        pageHrefs = ["http://dailymedi.com/"+tag.get('href') for tag in pageHrefTags]
        return pageHrefs

    def getPage(self, url):
        soup=Soup.requests(url)
        articleDate=re.sub("\D","",soup.find('font',color='#666666').get_text())[:8]
        articleID=articleDate[2:]+"_"+re.search("number=[0-9]*", url).group()[7:]
        articleTxt=soup.find('td', id='ct').get_text(separator="\n").strip()
        articleTitle=soup.find('div', id='sub_center_contents2').table.contents[7].table.contents[3].get_text().strip()
        return (articleID, articleDate, articleTitle, articleTxt)   