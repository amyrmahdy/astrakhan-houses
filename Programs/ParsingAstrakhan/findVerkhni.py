from selenium import webdriver
from bs4 import BeautifulSoup

def find_verkhine_stranitsi(LinkPage,driver):
    DictionLink = {LinkPage:1}
    while True:
        driver.get(LinkPage)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        infoLinks = soup.find_all('a',class_="_93444fe79c--list-itemLink--BU9w6")
        newLinks = 0
        for i in infoLinks:
            urlPage = i.get('href')
            if not ("cian.ru" in urlPage):
                urlPage = "https://astrahan.cian.ru"+urlPage
            if not (urlPage in DictionLink):
                DictionLink[urlPage]=1
                newLinks+=1
            else:
                DictionLink[urlPage]+=1
        if newLinks==0:
            break
        else:
            LinkPage=urlPage
    return DictionLink
