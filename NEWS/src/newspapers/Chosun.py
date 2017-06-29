from ..NewsCralwer import NewsCralwerInitializer
from ..NewsCralwer import NewsCralwerGetUrl
from ..Soup import Soup
import math
import re

class Chosun(NewsCralwerInitializer, NewsCralwerGetUrl):
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
        searchUrl = "http://search.chosun.com/search/news.search?query="+self.query+"&pageno=1&orderby=news&naviarraystr=%EC%B6%9C%EC%B2%98%26%26%5E%26%26categorynamenavigator%26%26%5E%26%26categoryname%26%26%5E%26%26%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4%26%26%5E%26%26%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4&&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=paging&sdate="+self.startDate+"&edate="+self.endDate+"&premium=#none"
        return self.searchUrl

    def getPageHrefs(self, count):
        searchUrl="http://search.chosun.com/search/news.search?query="+self.query+"&pageno="+str(count)+"&orderby=news&naviarraystr=%EC%B6%9C%EC%B2%98%26%26%5E%26%26categorynamenavigator%26%26%5E%26%26categoryname%26%26%5E%26%26%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4%26%26%5E%26%26%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4&&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=paging&sdate="+self.startDate+"&edate="+self.endDate+"&premium=#none"
        soup = Soup.requests(searchUrl)
        searchBox  =  soup.find("div", class_ = "result_box")
        pageHrefs = [ x.dt.a['href'] for x in resultBox.find_all("dl")]
        return pageHrefs

    def getPage(self, url):
        articleID=0
        articleDate = articleTitle = articleTxt = ""
        journeyType = _chkArticleType(url)

        if journeyType == "h" or journeyType == 'b':
            return (0,0,'chosun','0')

        if journeyType == 'v':
            soup = ArticleCralwer.getPhatomSoup(articleHref)
            articleTxt = soup.find("div",class_="par").get_text(separator = "\n\n").strip()
            articleDate=re.sub("\D","",articleHref)[:4]
            articleName=re.sub("\D","",articleHref)[2:]
            articleTitle=soup.find("div",class_="news_title_text").get_text().strip()

        elif journeyType == 'i':
            soup = ArticleCralwer.getReqSoup(articleHref)
            article = soup.find('div', id='news_body_id')    
            if article is None:
                #http://news.chosun.com/site/data/html_dir/2012/09/13/2012091302944.html
                articleTmp=soup.find('div', class_='article')
                try:
                    articleTmp.div.decompose()
                except AttributeError:
                    try:
                        articleTxt=soup.find('div',class_='par').get_text(separator="\n\n").strip()
                    except AttributeError:
                        articleTxt=""
                    articleTitle=soup.find('div',class_='news_title_text').get_text().strip()
                else:
                    articleTxtList = [x.get_text(separator="\n\n") for x in articleTmp.find_all('p')]
                    articleTxt= "\n".join(articleTxtList).strip()
                    articleTitle = soup.find("div",class_="title_author_2011").h2.get_text().strip()
            else:
                decomposeList = article.find_all('div',class_='news_date')+[article.ul]+article.find_all('div','ext_rel_article')+article.find_all('div',class_='news_imgbox')
                for a in article.find_all('a'):
                    a.unwrap()
                articleTxt=article.get_text(separator="\n\n").strip()
                articleTitle=soup.find("div",class_="news_title_text").h1.get_text().strip()
            dateAndName = re.sub("\D","",articleHref)
            articleDate=dateAndName[:4]
            articleName=dateAndName[-11:]
        else:
            print("error:%s"%articleHref)

        if len(articleTxt) < 3 :
            print("not script load %d"%i)
            articleTxt = "not script load"

        return (articleID, articleDate, articleTitle, articleTxt)     
    # check sub-chosun journeys
    def _chkArticleType(url):
        typeCheck = url[7]
        journeyType = ""
        if url[24] is 'v':
            journeyType = "svc"
        elif typeCheck is 'n':
            if url[11] is '.':
                journeyType = "news"
            else:
                journeyType = "newsteacher"
        elif typeCheck is 'b':
            if url[8] is 'i':
                journeyType = 'biz'
            elif url[8] is 'o':
                journeyType = 'books'
        elif typeCheck is 'h':
            journeyType = 'health'
        elif typeCheck is 'p':
            journeyType = "premium"
        elif typeCheck is 's':
            journeyType = 'senior'
        elif typeCheck is 'd':
            journeyType = 'danmee'
        return journeyType