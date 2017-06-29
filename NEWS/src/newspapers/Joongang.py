from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import re

class Joongang(NewsCralwerInitializer, NewsCralwerGetUrl):
    """description of class"""
    def setQuery(self, query):
        self.query = query
        return query
    def getQuery(self):
        return self.query
    def setDate(self, sDate, eDate): #yyyymmdd
        self.startDate = sDate 
        self.endDate = eDate 
    def __init__(self):
        pass
    def __init__(self, query, sDate, eDate):
        return super().__init__(query,sDate, eDate)

    def getPageCount(self):
        searchUrl = "http://search.joins.com/TotalNews?page=1&Keyword=" + self.query + "&StartSearchDate=" + self.startDate + "&EndSearchDate=" + self.endDate + "&SortType=New&SearchCategoryType=TotalNews&PeriodType=DirectInput&ScopeType=All&ServiceCode=&MasterCode=&SourceGroupType=Joongang&ReporterCode=&ImageType=All&JplusType=All&BlogType=All&ImageSearchType=Image&MatchKeyword=" + self.query + "&IncludeKeyword=&ExcluedeKeyword="
        soup = Soup.requests(searchUrl)
        pageCount = soup.find('span', class_="total_number").string
        return int(pageCount[2:].split(" ")[0])

    def getPageHrefs(self, count):
        searchUrl = "http://search.joins.com/TotalNews?page=" + str(count) + "&Keyword=" + self.query + "&StartSearchDate=" + self.startDate + "&EndSearchDate=" + self.endDate + "&SortType=New&SearchCategoryType=TotalNews&PeriodType=DirectInput&ScopeType=All&ServiceCode=&MasterCode=&SourceGroupType=Joongang&ReporterCode=&ImageType=All&JplusType=All&BlogType=All&ImageSearchType=Image&MatchKeyword=" + self.query + "&IncludeKeyword=&ExcluedeKeyword="
        soup = Soup.requests(searchUrl)
        searchBox = soup.find('ul', class_="list_default").find_all('li')
        pageHrefs = [x.find('a')['href'] for x in searchBox]
        return pageHrefs

    def getPage(self, url):
        soup = Soup.requests(url)
        if soup.find('div',class_='error'):
            print("Error Page : %s" % (url))
            return (0, "error", "error", 0)
        articleDate = re.sub("\D", "", soup.find('div',class_='byline').em.next_sibling.next_sibling.get_text())[:8]
        articleID = re.sub("\D", "", url)
        articleTitle = soup.find("",id='article_title').get_text().strip()
        # 강세, sub caption 등 중복되는 기사
        etc = soup.find_all('div',class_='ab_subtitle') + soup.find_all('div',class_='ab_related')+soup.find_all('span',class_='rt') + soup.find_all('a') + soup.find_all('td',class_='pt_8')
        photoCaption = soup.find_all('div', class_='html_photo_center') + soup.find_all('p',class_='caption') 
        for element in photoCaption+ etc:
            element.decompose()
        articleTxt = soup.find('div', id='article_body').get_text(separator="\n").strip()
        return (articleID, articleDate, articleTitle, articleTxt)

