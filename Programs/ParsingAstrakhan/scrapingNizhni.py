import time
import os
import json
import pandas as pd
from selenium import webdriver
from save_to_file import to_json
from kvartiri import find_kvartiri
from findDetailsNizhni import find_details_flats,find_multiIds
from secondLevelKeys import getSecondLevelKeys
from flats_to_pandas import flat_dict_to_pandas
from findVerkhni import find_verkhine_stranitsi
with open("input_links.txt","r") as f:
    input_string_all = f.read()
    begining_links = input_string_all.split("\n")
start = time.perf_counter()
driver = webdriver.Chrome()
dictionVerkhniFull = {}
for _ in range(2):
    for begining_link in begining_links:
        dictionVerkhniFull.update(find_verkhine_stranitsi(begining_link,driver))
    tempVerkhni = list(dictionVerkhniFull.keys()) 
    multiIds = find_multiIds(tempVerkhni,driver)
    begining_links = list(multiIds)
verkhniLinks = list(dictionVerkhniFull.keys())
if os.path.exists("verkhniLinks_NizhniVersion.json"):
    os.remove("verkhniLinks_NizhniVersion.json") 
to_json(dictionVerkhniFull,'verkhniLinks_NizhniVersion.json')
nizhniLinks = find_kvartiri(verkhniLinks,driver)
if os.path.exists("nizhniLinks_NizhniVersion.json"):
    os.remove("nizhniLinks_NizhniVersion.json") 
to_json(nizhniLinks,'nizhniLinks_NizhniVersion.json')
details = find_details_flats(list(nizhniLinks.keys()),driver)
if os.path.exists("details_NizhniVersion.json"):
    os.remove("details_NizhniVersion.json") 
to_json(details,'details_NizhniVersion.json')
data = flat_dict_to_pandas(details)
if os.path.exists("data_NizhniVersion.xlsx"):
    os.remove("data_NizhniVersion.xlsx") 
data.to_excel('data_NizhniVersion.xlsx',index = False)
finish = time.perf_counter()
print(f"Time performance was {finish-start} secondes")
