from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import math
import re
from urllib import parse

class Doctorsnews(NewsCralwerInitializer, NewsCralwerGetUrl):
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
        searchUrl="http://www.doctorsnews.co.kr/news/articleList.html?page=1&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_add_section_code=&sc_add_sub_section_code=&sc_add_serial_code=&sc_area=A&sc_level=&sc_m_level=&sc_article_type=&sc_view_level=&sc_sdate="+self.startDate+"&sc_edate="+self.endDate+"&sc_serial_number=&sc_word="+self.query+"&sc_word2=&sc_andor=OR&sc_order_by=I&view_type="
        soup = Soup.phantomjs(searchUrl)
        articleCnt = soup.find("tr", height="35").td.get_text()
        maxArticle =int(re.sub("\D","" ,articleCnt))
        return math.floor(int(maxArticle/25) )

    def getPageHrefs(self, count):
        searchUrl="http://www.doctorsnews.co.kr/news/articleList.html?page="+str(count)+"&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_add_section_code=&sc_add_sub_section_code=&sc_add_serial_code=&sc_area=A&sc_level=&sc_m_level=&sc_article_type=&sc_view_level=&sc_sdate="+self.startDate+"&sc_edate="+self.endDate+"&sc_serial_number=&sc_word="+self.query+"&sc_word2=&sc_andor=OR&sc_order_by=I&view_type="
        soupArticle = Soup.phantomjs(searchUrl)
        articleHrefList = soupArticle.find_all("a",class_="news_list_title")
        pageHrefs = ["http://www.doctorsnews.co.kr/news/"+x.get('href') for x in articleHrefList]
        return pageHrefs

    def getPage(self, url):
        articleID = re.sub("\D","",url)
        soup = Soup.requests(url)
        if soup.find('td', id='articleBody') is None:
            #본문이 없는 기사
            articleTitle = soup.find('b', class_='title').get_text()
            articleTxt = "사진 기사"
            articleDate = re.sub("\D","", soup.find('div', class_='info').get_text())[:8]
        else:
            #광고 제거
            adTags = soup.find('td', id='articleBody').find_all('table')
            for element in adTags:
                element.decompose()
            articleTxt = soup.find('td', id='articleBody').get_text(separator="\n").strip()
            articleDate = re.sub("\D","",soup.find('td', class_="WrtTip").get_text())[0:8]
            articleTitle = soup.find("td",id="font_title").get_text().strip()
        return (articleID, articleDate, articleTitle, articleTxt)

