from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import math
import re

class Donga(NewsCralwerInitializer, NewsCralwerGetUrl):
    def setQuery(self, query):
        self.query = query
        return
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
        searchUrl="http://news.donga.com/search?p=1&query="+self.query+"&check_news=1&more=1&sorting=1&search_date=1&v1="+self.startDate+"&v2="+self.endDate+"&range=1"
        soup = Soup.requests(searchUrl)
        return math.floor(int(re.sub('\D',"", soup.find('div',class_="searchCont").h2.span.text ))//15)

    def getPageHrefs(self, count):
        # 동아일보만 검색되게??? 나머지는???
        searchUrl="http://news.donga.com/search?p="+str(count)+"&query="+self.query+"&check_news=1&more=1&sorting=1&search_date=1&v1="+self.startDate+"&v2="+self.endDate+"&range=1"
        soup = Soup.requests(searchUrl)
        searchBox = soup.find_all("div", class_="searchList")
        pageHrefs = [element.div.a['href'] for element in searchBox]
        return pageHrefs

    def getPage(self, url):                
        articleID = url[37:-2]
        articleDate = url[28:36] #yyyymmdd
        if articleDate.isdigit() is False:
            #date error
            return -1
        articleSoup =  Soup.requests(url)
        article = articleSoup.find('div', class_='article_txt')
        for script in article.find_all('script'):
            script.extract()

        adTags = article.find_all('div', class_='article_relation') + article.find_all('span',class_='t')
        photoCaption = article.find_all('div',class_='articlePhotoC') +article.find_all('div',class_='articlePhotoB') + article.find_all('div',class_='articlePhotoA')
        notArticleTxt = adTags + photoCaption
        for element in notArticleTxt:
            element.decompose()
        articleTxt = article.get_text(separator="\n").strip()
        articleTitle = articleSoup.find('div', class_='article_title').find(class_='title').get_text().strip()
        return (articleID, articleDate, articleTitle, articleTxt)