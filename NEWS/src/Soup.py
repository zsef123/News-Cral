from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

class Soup(object):
    """description of class"""
    def requests(url, parser='lxml', encoding='utf8', timeout=60):
        try:
            page = requests.get(url, timeout=timeout)
            if encoding is not 'utf8':
                page.encoding = encoding
                soup = BeautifulSoup(page.text, parser)
            else:
                soup = BeautifulSoup(page.content, parser)
        except requests.exceptions.Timeout:
            print("\nTimeout occurred : %s\n"%articleHref)
        return soup
    def phantomjs(url,parser='lxml', dir="phantomjs.exe", timeout=60):
        browser = webdriver.PhantomJS(executable_path=dir,service_args=['--ignore-ssl-errors=true'])
        browser.implicitly_wait(timeout)
        browser.set_script_timeout(timeout)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, parser)
        browser.quit()
        return soup

