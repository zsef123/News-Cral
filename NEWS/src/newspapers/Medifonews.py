from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
from urllib import parse
import re
import math

class Medifonews(NewsCralwerInitializer, NewsCralwerGetUrl):
    """description of class"""
    def setQuery(self, query):
        self.query = parse.quote(query)
        return self.query
    def getQuery(self):
        return parse.unquote(self.query)
    def setDate(self, sDate, eDate): #yyyymmdd
        self.startDate = sDate[:4] + '-' + sDate[4:6] + '-' + sDate[6:]
        self.endDate = eDate[:4] + '-' + eDate[4:6] + '-' + eDate[6:]
    def __init__(self):
        pass
    def __init__(self, query, sDate, eDate):
        return super().__init__(query,sDate, eDate)

    def getPageCount(self):
        searchUrl = "http://medifonews.com/news/search_result.html?search=" + self.query + "&search_mode=&hash=&s_title=&s_writer_name=&s_body=&s_sdate=" + self.startDate + "&s_edate=" + self.endDate + "&page=1"
        soup = Soup.requests(searchUrl)
        maxPageCnt = int(soup.find('i',class_='t02').get_text())
        return math.floor(maxPageCnt / 20)

    def getPageHrefs(self, count):
        searchUrl = "http://medifonews.com/news/search_result.html?search=" + self.query + "&search_mode=&hash=&s_title=&s_writer_name=&s_body=&s_sdate=" + self.startDate + "&s_edate=" + self.endDate + "&page=" + str(count)
        soup = Soup.requests(searchUrl)
        searchBox = soup.find('ul', class_='art_list_all').find_all('a')
        pageHrefs = ["http://medifonews.com/news/" + x.get('href') for x in searchBox]
        return pageHrefs

    def getPage(self, url):
        soup = Soup.requests(url)
        articleID = re.sub("\D","",url)
        articleTitle = soup.find('div',class_='art_top').h2.get_text().strip()
        articleDate = re.sub("\D","",soup.find('ul',class_='art_info').contents[3].get_text())[:8]
        articleTxt = soup.find('div',id='news_body_area').get_text(separator="\n").strip()
        return (articleID, articleDate, articleTitle, articleTxt)

