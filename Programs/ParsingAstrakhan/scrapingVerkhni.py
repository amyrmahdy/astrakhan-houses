import time
import json
import os
import pandas as pd
from selenium import webdriver
from findDetailsVerkhni import find_details_flats
from findVerkhni import find_verkhine_stranitsi
from secondLevelKeys import getSecondLevelKeys
from flats_to_pandas import flat_dict_to_pandas
from save_to_file import to_json

with open("input_links.txt","r") as f:
    input_string_all = f.read()
    begining_links = input_string_all.split("\n")

details = {}
start = time.perf_counter()
driver = webdriver.Chrome()
lastMultiIdsNumb = 0
for _ in range(2):
    dictionVerkhniFull = {}
    for begining_link in begining_links:
        dictionVerkhniFull.update(find_verkhine_stranitsi(begining_link,driver))
    verkhniLinks = list(dictionVerkhniFull.keys())   
    details, multiIds = find_details_flats(verkhniLinks,details,driver)
    begining_links = list(multiIds)
   
driver.quit()
if os.path.exists("verkhniLinks_VerkhniVersion.json"):
    os.remove("verkhniLinks_VerkhniVersion.json") 
to_json(dictionVerkhniFull,'verkhniLinks_VerkhniVersion.json')
if os.path.exists("details_VerkhniVersion.json"):
    os.remove("details_VerkhniVersion.json") 
to_json(details,'details_VerkhniVersion.json')
data = flat_dict_to_pandas(details)
if os.path.exists("data_VerkhniVersion.xlsx"):
    os.remove("data_VerkhniVersion.xlsx") 
data.to_excel('data_VerkhniVersion.xlsx',index = False)
finish = time.perf_counter()
print(f"Time performance was {finish-start} secondes")
