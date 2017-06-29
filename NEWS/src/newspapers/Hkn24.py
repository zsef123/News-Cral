from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import math
import re
from urllib import parse

class Hkn24(NewsCralwerInitializer, NewsCralwerGetUrl):
    """description of class"""
    def setQuery(self, query):
        return super().setQuery(query)
    def getQuery(self):
        return super().getQuery()
    def setDate(self, sDate, eDate): #yyyymmdd
        #날짜 검색 불가
        return
    def __init__(self):
        pass
    def __init__(self, query, sDate, eDate):
        return super().__init__(query,sDate, eDate)

    def getPageCount(self):
        searchUrl = "http://www.hkn24.com/news/articleList.html?page=1&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word="+self.query+"&sc_view_code=&view_type="
        soup = Soup.phantomjs(searchUrl)
        pageCount= int(re.sub("\D","",soup.find('font', color='#333333').get_text()))
        return math.floor(pageCount/20)

    def getPageHrefs(self, count):
        searchUrl = "http://www.hkn24.com/news/articleList.html?page="+str(count)+"&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word="+self.query+"&sc_view_code=&view_type="
        soup = Soup.phantomjs(searchUrl)
        searchBox = soup.find_all('td', class_='ArtList_Title')
        pageHrefs = ["http://www.hkn24.com/news/"+x.a.get('href') for x in searchBox]
        return pageHrefs

    def getPage(self, url):
        soup=Soup.requests(url)
        articleID=re.sub("\D","",url)[2:]
        articleDate=re.sub("\D","", soup.find('div',class_='View_Time').get_text())[:8]
        articleTitle=soup.find('div',class_='View_Title').strong.get_text().strip()
        
        adTags = soup.find('div',id='CmAdContent').find_all('table')
        for element in adTags:
            element.decompose()
        articleTxt=soup.find('div',id='CmAdContent').get_text(separator="\n").strip()
        return (articleID, articleDate, articleTitle, articleTxt)

