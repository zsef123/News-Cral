from src.NewsCralwer import NewsCralwerInitializer
from src.NewsCralwer import NewsCralwerGetUrl
from src.Soup import Soup
import re
import math 

class Nursenews(NewsCralwerInitializer, NewsCralwerGetUrl):
    """description of class"""
    def setQuery(self, query):
        return super().setQuery(query)
    def getQuery(self):
        return super().getQuery()
    def setDate(self, sDate, eDate): #yyyymmdd
        #검색불가
        return
    def __init__(self):
        pass
    def __init__(self, query, sDate, eDate):
        return super().__init__(query,sDate, eDate)

    def getPageCount(self):
        searchUrl = "http://www.nursenews.co.kr/main/search.asp?SearchStr="+self.query+"&intPage=1"
        soup=Soup.requests(searchUrl)
        pageCount =int(re.sub("\D","",soup.find_all("img", align="absmiddle")[1].parent.get('href')[-3:]))
        return pageCount

    def getPageHrefs(self, count):
        searchUrl = "http://www.nursenews.co.kr/main/search.asp?SearchStr="+self.query+"&intPage="+str(count)
        soup=Soup.requests(searchUrl)
        searchBox = soup.find('ul',class_='ul_board').find_all('li')
        pageHrefs = ["http://www.nursenews.co.kr/main"+x.a.get('href')[1:] for x in searchBox]
        return pageHrefs

    def getPage(self, url):
        soup=Soup.requests(url)        
        articleID=re.search("idx=[0-9]*",url).group()[4:]
        articleDate=re.search("[12][0-9]{3}-[0-9]{2}-[0-9]{2}",soup.find('div',class_='txt_1').get_text()).group() # need 
        articleDate=re.sub("\D","", articleDate)
        #주석 제거
        for x in soup.find('div',id='neyongID').find_all('span'):
            x.decompose()
        articleTxt=soup.find('div',id='neyongID').get_text(separator="\n").strip()

        titleTag=soup.find('div',class_='bx_board').find('div',class_='tit_1')
        articleSubTitle=titleTag.find('div',class_='txt_s')
        articleSubTitle.decompose()
        articleTitle=titleTag.get_text().strip()
        return (articleID, articleDate, articleTitle, articleTxt)

