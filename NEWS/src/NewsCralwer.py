import abc
from urllib import parse
"""
크롤링 단계에는 무엇이있나
1. 검색 옵션 조절
2. 검색 시행
3. 결과 리스트 만들기(한 페이지에 보이는 기사)
4. 기사 탐색
5. 페이지 넘어간 후 3번 시행
"""
class NewsCralwerInitializer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def setQuery(self,query):
        self.query = parse.quote(query.encode('cp949'))
        return self.query    
    @abc.abstractmethod
    def getQuery(self):
        return parse.unquote(self.query, 'cp949')
    @abc.abstractmethod
    def setDate(self,sDate,eDate):
        pass
    @abc.abstractmethod
    def __init__(self,query,sDate,eDate):
        self.setQuery(query)
        self.setDate(sDate, eDate)
        return

class NewsCralwerGetUrl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getPageCount(self, url):
        pass
    @abc.abstractmethod
    def getPageHrefs(self, url, count):
        pass
    @abc.abstractmethod
    def getPage(self, url):
        pass