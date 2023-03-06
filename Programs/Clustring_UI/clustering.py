import os
import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from functions import clean_dataFrame,preprocessing,predict_price
from functions_dbscan import plot_location_dbscan
from functions_sobstveni import plot_my_alg

tipDomPerevod = {
    "кирпичный": "brick",
    "монолитный":"monolith",
    "монолитно-кирпичный":"monolithBrick",
    "панельный":"panel",
    "блочный":"block",
    "не важно": "не важно"
}

tipRemontPerevod = {
        "не важно": "не важно",
        "без ремонта": "no" ,
        "косметический" : "cosmetic",
        "евроремонт" : "euro",
        "дизайнерский" : "design"
}

def general(signal,minArea,maxArea,tip_doma,tip_remont,epsilon,algorithm):
    try:
        pd.options.mode.chained_assignment = None
        df = pd.read_excel("data_estimatedPrice_20may_astrakhan.xlsx")
        df = clean_dataFrame(df)
        estimatedTrue,estimatedFalse = preprocessing(df,minArea,maxArea,tipDomPerevod[tip_doma],tipRemontPerevod[tip_remont])
        if algorithm == "DBSCAN":
            df_clustered,df_target_clustered = plot_location_dbscan(estimatedTrue,estimatedFalse,signal,epsilon)
        elif algorithm == "Мой алгоритм":
            df_clustered,df_target_clustered = plot_my_alg(estimatedTrue,estimatedFalse,signal,epsilon)    
        mean_each_cluster = df_clustered.groupby(['кластер']).mean()['цена за кв м'].copy()
        std =  df_clustered.groupby(['кластер']).std()['цена за кв м'].copy()
        df_price = predict_price(df_target_clustered,mean_each_cluster)
        count_each_cluster = df_clustered.groupby(['кластер']).count().copy()
        count_each_cluster = count_each_cluster.reset_index()
        details = count_each_cluster[['кластер','url']]
        details.columns = ['кластер','количество элементов']
        details['Среднее значение'] = mean_each_cluster.copy()
        details['Среднее отклонение'] = std.copy()
        df_clustered = df_clustered.sort_values(by = ['кластер'])
        df_clustered = df_clustered.reset_index(drop=True)
        df_price['кластер'] = df_price['кластер'].astype(int)
        df_price = df_price.sort_values(by = ['кластер'])
        df_price = df_price.reset_index(drop=True)
        df_price['цена за кв м'] = df_price['предсказание'] / df_price['общ. площадь']
        df_price['цена за кв м'] =  df_price['цена за кв м'].astype(int)
        dfs = [df_clustered,df_price]
        mix_df = pd.concat(dfs)
        mix_df = mix_df.reset_index(drop = True)
        if algorithm == "DBSCAN" and signal not in [0,1,2]:    
        
            if signal == 3:                
                details.to_excel("details_dbscan.xlsx", index = False)
                if platform.system() == "Linux":
                    os.system("xdg-open details_dbscan.xlsx")
                else:
                    os.system("start details_dbscan.xlsx")
                    
            elif signal == 4:
                df_clustered.to_excel("base_clustering_dbscan.xlsx", index = False)
                if platform.system() == "Linux":
                    os.system("xdg-open base_clustering_dbscan.xlsx")
                else:
                    os.system("start base_clustering_dbscan.xlsx")
                    
            elif signal == 5:
                df_price.to_excel("predict_price_dbscan.xlsx", index = False)
                if platform.system() == "Linux":
                    os.system("xdg-open predict_price_dbscan.xlsx")
                else:
                    os.system("start predict_price_dbscan.xlsx")
       
            elif signal == 6:
                mix_df.to_excel("mixed_dbscan.xlsx", index = False)
                if platform.system() == "Linux":
                    os.system("xdg-open mixed_dbscan.xlsx")
                else:
                    os.system("start mixed_dbscan.xlsx")

        elif algorithm == "Мой алгоритм" and signal not in [0,1,2]:
            if signal == 3:                
                details.to_excel("details_my_alg.xlsx", index = False)
                if platform.system() == "Linux":
                    os.system("xdg-open details_my_alg.xlsx")
                else:
                    os.system("start details_my_alg.xlsx")
                    
            elif signal == 4:
                df_clustered.to_excel("base_clustering_my_alg.xlsx", index = False)
                if platform.system() == "Linux":
                    os.system("xdg-open base_clustering_my_alg.xlsx")
                else:
                    os.system("start base_clustering_my_alg.xlsx")
                    
            elif signal == 5:
                df_price.to_excel("predict_price_my_alg.xlsx", index = False)
                if platform.system() == "Linux":
                    os.system("xdg-open predict_price_my_alg.xlsx")
                else:
                    os.system("start predict_price_my_alg.xlsx")
       
            elif signal == 6:
                mix_df.to_excel("mixed_my_alg.xlsx", index = False)
                if platform.system() == "Linux":
                    os.system("xdg-open mixed_my_alg.xlsx")
                else:
                    os.system("start mixed_my_alg.xlsx")
    except Exception as ex:
        print("Error in clustering")
        print(ex)


