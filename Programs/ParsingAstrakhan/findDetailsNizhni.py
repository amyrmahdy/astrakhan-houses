import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from findDetails import getComposeKey,noneObjects,getDictByTemplate

data_keys_script1 = [["page","dealType"],
                     ["page","objectType"],
                     ["products","[","objectType"],
                     ["products","[","dealType"],
                     ["products","[","cianId"],
                     ["products","[","photosCount"],
                     ["products","[","podSnos"],
                     ["products","[","price"],
                     ["products","[","published"],
                     ["products","[","variant","["],
                     ]

data_keys_script2 = [
            ["value","offerData","offer","geo","{","address","type","locationTypeId","fullName"],
            ["value","offerData","offer",'floorNumber'],
            ["value","offerData","offer",'deadline','quarterEnd'],
            ["value","offerData","offer",'deadline','quarter'],
            ["value","offerData","offer",'deadline','isComplete'],
            ["value","offerData","offer",'deadline','year'],             
            ["value","offerData","offer",'newbuilding','house','name'],
            ["value","offerData","offer",'newbuilding','house','isFinished'],
            ["value","offerData","offer",'newbuilding','house','finishDate','quarter'],
            ["value","offerData","offer",'newbuilding','house','finishDate','year'],
            ["value","offerData","offer",'newbuilding','isFromSeller'],
            ["value","offerData","offer",'newbuilding','name'],
            ["value","offerData","offer",'newbuilding','isFromBuilder'],
            ["value","offerData","offer",'newbuilding','isFromDeveloper'],
            ["value","offerData","offer",'newbuilding','newbuildingFeatures',"videosCount"],
            ["value","offerData","offer",'newbuilding','newbuildingFeatures',"deadlineInfo"],
            ["value","offerData","offer",'newbuilding','newbuildingFeatures',"reviewsCount"],
            ["value","offerData","offer",'newbuilding','newbuildingFeatures',"imagesCount"],
            ["value","offerData","offer",'geo','coordinates','lat'],
            ["value","offerData","offer",'geo','coordinates','lng'],             
            ["value","offerData","offer",'building','floorsCount'],
            ["value","offerData","offer",'building','materialType'],
            ["value","offerData","offer",'building','totalArea'],
            ["value","offerData","offer",'building','cargoLiftsCount'],
            ["value","offerData","offer",'building','passengerLiftsCount'],
            ["value","offerData","offer",'building','hasGarbageChute'],
            ["value","offerData","offer",'building','ceilingHeight'],
            ["value","offerData","offer",'building','deadline',"quarterEnd"],
            ["value","offerData","offer",'building','deadline',"quarter"],
            ["value","offerData","offer",'building','deadline',"isComplete"],
            ["value","offerData","offer",'building','deadline',"year"],
            ["value","offerData","offer",'offerType'],
            ["value","offerData","offer",'separateWcsCount'],
            ["value","offerData","offer",'combinedWcsCount'],
            ["value","offerData","offer",'balconiesCount'],
            ["value","offerData","offer",'windowsViewType'],
            ["value","offerData","offer",'cargoLiftsCount'],
            ["value","offerData","offer",'passengerLiftsCount'],
            ["value","offerData","offer",'loggiasCount'],
            ["value","offerData","offer",'hasParking'],
            ["value","offerData","offer",'description'],
            ["value","offerData","offer",'totalArea'], 
            ["value","offerData","offer",'repairType'], 
            ["value","offerData","offer",'kitchenArea'],
            ["value","offerData","offer",'status'],        
            ["value","offerData","offer",'roomsCount'],
            ["value","offerData","offer",'livingArea'],     
            ["value","offerData","offer",'bargainTerms','prices',"rur"],
            ["value","offerData","offer",'bargainTerms','prices',"usd"],
            ["value","offerData","offer",'bargainTerms','prices',"eur"],
            ["value","offerData","offer",'bargainTerms','price'],
            ["value","offerData",'costEstimationData','estimatedPrice'],            
            ["value","offerData",'bti','houseData','floorMax'],
            ["value","offerData",'bti','houseData','entrances'],
            ["value","offerData",'bti','houseData','seriesName'],
            ["value","offerData",'bti','houseData','houseGasSupplyType'],
            ["value","offerData",'bti','houseData','yearRelease'],
            ["value","offerData",'bti','houseData','houseMaterialType'],
            ["value","offerData",'bti','houseData','demolishedInMoscowProgramm'],
            ["value","offerData",'bti','houseData','houseHeatSupplyType'],
            ["value","offerData",'bti','houseData','isEmergency'],
            ["value","offerData",'bti','houseData','houseOverhaulFundType'],
            ["value","offerData",'bti','houseData','houseOverlapType'],
            ["value","offerData",'bti','houseData','lifts'],
            ["value","offerData",'bti','houseData','flatCount'],
            ["value",'tracking','page','dealType'],
            ["value",'tracking','page','objectType']
            ]
    
def find_details_flats(links,driver):
    bigDict = {}
    for link in links:
        try:
            tempDict = find_details_flat(link,driver)
            bigDict[link] = tempDict
        except:
            print(link)
    driver.quit()
    return bigDict



def find_details_flat(link,driver):
    tempDict = {}
    driver.get(link)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    pattern_senario1 = re.compile('ca\(\"pageviewSite\",(.*?)\)')
    script_1 = soup.find('script',text = pattern_senario1)
    script_1_found = pattern_senario1.search(script_1.text)    
    beforJsonScript1 = script_1_found.group(1)
    jsonScript1 = json.loads(beforJsonScript1)

    pattern_senario2 =re.compile( 'frontend-offer-card\'] = (.*?)];')
    script_2 = soup.find('script',text = pattern_senario2)
    script_2_found = pattern_senario2.search(script_2.text)
    beforJsonScript2 = script_2_found.group(1)+']'
    jsonScript2 = json.loads(beforJsonScript2)
    for i in jsonScript2:
        if i['key'] == 'defaultState':
            jsonScript2Final = i
            break

    for data_key in data_keys_script1:
        microDict=getDictByTemplate(jsonScript1,data_key)
        for key in microDict:            
            if key in tempDict:
                print("Error on page:", link, "Template:", data_key, "Key:",key)
            else:
                tempDict[key] = microDict[key]
    for data_key in data_keys_script2:
        microDict=getDictByTemplate(jsonScript2Final,data_key)
        for key in microDict:            
            if key in tempDict:
                print("Error on page:", link, "Template:", data_key, "Key:",key)
            else:
                tempDict[key] = microDict[key]
    return tempDict



def find_multiIds(links,driver):
    multiIds = set()
    for link in links:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        pattern_senario2 =re.compile( 'frontend-serp\'] = (.*?)];')
        script_2 = soup.find('script',text = pattern_senario2)
        script_2_found = pattern_senario2.search(script_2.text)
        beforJsonScript2 = script_2_found.group(1)+']'
        jsonScript2 = json.loads(beforJsonScript2)

        for miniDict in jsonScript2:
            if miniDict["key"] == "initialState":
                jsonScript2Final = miniDict["value"]["results"]["offers"]
                break
        for kvartir in jsonScript2Final:
            similar = kvartir['similar']
            if similar is not None:
                url = similar['url']
                multiIds.add("https://astrahan.cian.ru"+ url)
    return multiIds
