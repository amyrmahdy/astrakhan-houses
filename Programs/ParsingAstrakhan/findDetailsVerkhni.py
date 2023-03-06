import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from findDetails import getComposeKey,noneObjects,getDictByTemplate


data_keys_script1 = [["objectType"],
                     ["dealType"],
                     ["photosCount"],
                     ["podSnos"],
                     ["price"],
                     ["published"],
                     ["variant","["]
                     ]
data_keys_script2 = [
            ["cianId"],
            ['geo','coordinates','lat'],
            ['geo','coordinates','lng'], 
            ["geo","{","address","type","locationTypeId","fullName"],
            ['floorNumber'],
            ['newbuilding','house','name'],
            ['newbuilding','house','isFinished'],
            ['newbuilding','house','finishDate','quarter'],
            ['newbuilding','house','finishDate','year'],
            ['newbuilding','isFromSeller'],
            ['newbuilding','name'],
            ['newbuilding','isFromBuilder'],
            ['newbuilding','isFromDeveloper'],
            ['building','floorsCount'],
            ['building','materialType'],
            ['building','deadline',"quarterEnd"],
            ['building','deadline',"quarter"],
            ['building','deadline',"isComplete"],
            ['building','deadline',"year"],
            ['offerType'],
            ['totalArea'],
            ['kitchenArea'],
            ['status'],        
            ['roomsCount'],
            ['flatType'],
            ['livingArea'],     
            ['bargainTerms','price'],
            ["added"],
            ["similar","url"]         
            ]

def find_details_flats(links,bigDict,driver):
    multiIds = set()
    for link in links:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source,'html.parser')
            
        pattern_senario1 = re.compile('"products":(.*?)}}\]')
        script_1 = soup.find('script',text = pattern_senario1)
        script_1_found = pattern_senario1.search(script_1.text)    
        beforJsonScript1 = script_1_found.group(1) + "}}]"
        jsonScript1 = json.loads(beforJsonScript1)

        pattern_senario2 =re.compile( 'frontend-serp\'] = (.*?)];')
        script_2 = soup.find('script',text = pattern_senario2)
        script_2_found = pattern_senario2.search(script_2.text)
        beforJsonScript2 = script_2_found.group(1)+']'
        jsonScript2 = json.loads(beforJsonScript2)

        for kvartir in jsonScript1:
            tempDict = {}
            for data_key in data_keys_script1:
                tempDict.update(getDictByTemplate(kvartir,data_key))
            bigDict[kvartir["cianId"]] = tempDict
        for miniDict in jsonScript2:
            if miniDict["key"] == "initialState":
                jsonScript2Final = miniDict["value"]["results"]["offers"]
                break
        for kvartir in jsonScript2Final:
            tempDict = {}
            for data_key in data_keys_script2:
                tempDict.update(getDictByTemplate(kvartir,data_key))
            if tempDict["similarurl"] is not None:                 
                multiIds.add("https://astrahan.cian.ru"+ tempDict["similarurl"])
            bigDict[kvartir["cianId"]].update(tempDict)
    return bigDict,multiIds
