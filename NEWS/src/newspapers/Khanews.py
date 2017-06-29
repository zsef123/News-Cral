from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import re
import math

class Khanews(NewsCralwerInitializer, NewsCralwerGetUrl):
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
        searchUrl="http://www.khanews.com/news/articleList.html?page=&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=2000.01.01&sc_edate=&sc_serial_number=&sc_word="+self.query+"&view_type="
        soup = Soup.phantomjs(searchUrl)
        tbodys = soup.find("td", bgcolor="#FFFFFF")
        pageCount =int(re.sub("\D","" ,tbodys.find("font",color="#333333").get_text()))
        return math.floor(pageCount/20)

    def getPageHrefs(self, count):
        searchUrl="http://www.khanews.com/news/articleList.html?page="+str(count)+"&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=2000.01.01&sc_edate=&sc_serial_number=&sc_word="+self.query+"&view_type="
        soup = Soup.phantomjs(searchUrl)
        searchBox = soup.find("td", bgcolor="#FFFFFF").find_all("font", color="#001DD0")
        pageHrefs = ["http://www.khanews.com/news/"+x.parent.get('href') for x in searchBox]
        return pageHrefs

    def getPage(self, url):
        soup = Soup.requests(url)
        photoCaption = soup.find('td', id='articleBody').find_all('table')
        for element in photoCaption:
            element.decompose()
        articleTxt = soup.find('td', id='articleBody').get_text(separator="\n").strip()
        articleDate = re.sub("\D","",soup.find('td', bgcolor="EFEFEF").get_text())[:8]
        articleID = articleDate[2:]+"_"+re.sub("\D","",url)
        articleTitle = soup.find("td",class_="view_t").get_text().strip()
        return (articleID, articleDate, articleTitle, articleTxt)

