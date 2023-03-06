import os
import math
import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


m = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o','o',
    '^', '^', '^', '^', '^', '^', '^','^', '^','^',
    's', 's', 's', 's', 's', 's', 's', 's', 's','s',
    'D', 'D', 'D', 'D', 'D', 'D', 'D','D', 'D','D',
    'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H','H',
    'p','p', 'p', 'p', 'p', 'p', 'p', 'p', 'p','p',
    'v', 'v', 'v', 'v', 'v', 'v', 'v','v', 'v','v',
    ]


def clean_dataFrame(df):
    df = df[[ "url","productsobjectType",
        "valueofferDataofferbargainTermspricesrur",
        "valueofferDataofferbuildingfloorsCount",
        "valueofferDataofferbuildingmaterialType",
        "valueofferDataofferbuildingtotalArea",
        "valueofferDataofferfloorNumber",
        "valueofferDataoffergeocoordinateslat",
        "valueofferDataoffergeocoordinateslng",
        "valueofferDataofferkitchenArea",
        "valueofferDataofferlivingArea",
        "valueofferDataofferroomsCount",
        "valueofferDataofferrepairType",
        "valueofferDatabtihouseDatayearRelease",
        "valueofferDatacostEstimationDataestimatedPrice"]]
    df = df.rename(columns={
        "productsobjectType": "objectType",
        "valueofferDataofferbargainTermspricesrur":"цена",
        "valueofferDataofferbuildingfloorsCount":"кол. этажей",
        "valueofferDataofferbuildingmaterialType":"тип дома",
        "valueofferDataofferbuildingtotalArea":"общ. площадь",
        "valueofferDataofferfloorNumber":"этаж",
        "valueofferDataoffergeocoordinateslat":"широта",
        "valueofferDataoffergeocoordinateslng":"долгота",
        "valueofferDataofferkitchenArea":"площадь кухни",
        "valueofferDataofferlivingArea":"жил. площадь",
        "valueofferDataofferroomsCount":"кол. комнат",
        "valueofferDataofferrepairType":"тип ремонта",
        "valueofferDatabtihouseDatayearRelease" : "год постройки",
        "valueofferDatacostEstimationDataestimatedPrice":"оценка cian"
        })
    df["оценка cian"] = df['оценка cian'].str.replace("₽","")
    df["оценка cian"] = df['оценка cian'].str.replace("\xa0","")
    df["оценка cian"] = df["оценка cian"].astype(float)
    return df


def preprocessing(df,total_area_min,total_area_max,tip_doma,tip_remont):  
    if tip_doma != "не важно" and tip_remont != "не важно":
        df = df.loc[ 
            (df['общ. площадь']>=total_area_min) & 
            (df['общ. площадь']<=total_area_max) & 
            (df['тип дома']==tip_doma) &
            (df['тип ремонта']==tip_remont)
            ].reset_index(drop=True).copy()
    elif tip_doma == "не важно" and tip_remont == "не важно":
        df = df.loc[ 
            (df['общ. площадь']>=total_area_min) & 
            (df['общ. площадь']<=total_area_max)
            ].reset_index(drop=True).copy()
    elif tip_doma != "не важно" and tip_remont == "не важно":
        df = df.loc[ 
            (df['общ. площадь']>=total_area_min) & 
            (df['общ. площадь']<=total_area_max) & 
            (df['тип дома']==tip_doma)
            ].reset_index(drop=True).copy()
    elif tip_doma == "не важно" and tip_remont != "не важно":
        df = df.loc[ 
            (df['общ. площадь']>=total_area_min) & 
            (df['общ. площадь']<=total_area_max) & 
            (df['тип ремонта']==tip_remont)
            ].reset_index(drop=True).copy()
    df = df[['url','общ. площадь','оценка cian','широта','долгота','тип дома','тип ремонта']].copy()
    if df.shape[0] > 2:
        estimatedFalse = df[df["оценка cian"].isna()].copy()
        estimatedTrue = df[df["оценка cian"].notna()].copy()
        estimatedTrue["цена за кв м"] = df["оценка cian"] / df["общ. площадь"]
        estimatedTrue,estimatedFalse = estimatedTrue.reset_index(drop=True).copy(),estimatedFalse.reset_index(drop=True).copy() 
        return estimatedTrue,estimatedFalse
    else:
        print("NOT FOUND ENOUGH ELEMENTS")



def predict_price(df,mean):
    prices = [-1] * df.shape[0]
    for i in range(df.shape[0]):
        if df.loc[i]["кластер"] != -1:
            prices[i] = int(df.loc[i]["общ. площадь"] * mean[df.loc[i]["кластер"]])
    df["предсказание"] = prices
    return df

