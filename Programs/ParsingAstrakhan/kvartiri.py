from selenium import webdriver
from bs4 import BeautifulSoup
def find_kvartiri(x,driver):
    AllLinksDic={}
    for z in x:
        AllLinksFromPages=[]
        driver.get(str(z))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        AllLinksFromPages = soup.find_all('a',class_="_93444fe79c--link--eoxce")        
        for i in AllLinksFromPages:
            flatLink = i.get('href')
            if not (flatLink in AllLinksDic):
                AllLinksDic[flatLink]=1
            else:
                AllLinksDic[flatLink]+=1
    return AllLinksDic

