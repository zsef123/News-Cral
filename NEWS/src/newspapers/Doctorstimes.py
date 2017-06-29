from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import math
import re
from urllib import parse

class Doctorstimes(NewsCralwerInitializer, NewsCralwerGetUrl):
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
        searchUrl = "http://www.doctorstimes.com/news/articleList.html?page=1&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word="+self.query+"&sc_word2=&sc_andor=&sc_order_by=E&view_type="
        soup = Soup.phantomjs(searchUrl)
        pageCount = int(re.sub("\D","",soup.select("#article-list > tbody > tr > td > table > tbody > tr:nth-of-type(1) > td > table > tbody > tr > td:nth-of-type(1)")[0].get_text()))
        return math.floor(pageCount/20)

    def getPageHrefs(self, count):
        searchUrl = "http://www.doctorstimes.com/news/articleList.html?page="+str(count)+"&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word="+self.query+"&sc_word2=&sc_andor=&sc_order_by=E&view_type="
        soup = Soup.phantomjs(searchUrl,'html.parser')
        searchBox = soup.find_all('td',class_='list-titles list-pad-5')
        pageHrefs = ["http://www.doctorstimes.com/news/"+x.a.get('href') for x in searchBox]
        return pageHrefs

    def getPage(self, url):
        soup = Soup.requests(url)
        if soup.find('div', id='articleBody') is None:
            articleTxt="사진 기사"
            articleDate=re.sub("\D","", soup.select("#ND_Warp > table:nth-of-type(2)")[0].get_text())
            articleTitle=soup.select("#ND_Warp > table:nth-of-type(1) > tr > td:nth-of-type(2)")[0].get_text().strip()
        else:
            adTags = soup.find('div', id='articleBody').find_all('table')
            for element in adTags:
                element.decompose()
            articleTxt=soup.find('div', id='articleBody').get_text(separator="\n").strip()
            articleDate=re.sub("\D","",soup.find('div',class_="info").contents[7].get_text())[:8]
            articleTitle=soup.find('span',class_='headline-title').get_text().strip()
        articleID=str(articleDate[2:]+re.sub("\D","",url))
        return (articleID, articleDate, articleTitle, articleTxt)