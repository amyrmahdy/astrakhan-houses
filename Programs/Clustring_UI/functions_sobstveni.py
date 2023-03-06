import os
import math
import numpy as np
import pandas as pd
import seaborn
import mplcursors
import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from functions import m,predict_price

matplotlib.use('Qt5Agg')


#MY ALGORITHM
def my_algorithm(df,threshold):
    cluster = []
    center_cluster = []
    cluster.append(0) 
    center_cluster.append([df.loc[0]['широта'],df.loc[0]['долгота']])
    for i in range(1,df.shape[0]):
        min_dist = math.dist([df.loc[i]['широта'],df.loc[i]['долгота']],[df.loc[0]['широта'],df.loc[0]['долгота']])
        cluster.append(0)
        for j in range(len(center_cluster)):
            if math.dist([df.loc[i]['широта'],df.loc[i]['долгота']],center_cluster[j]) < min_dist:
                min_dist =  math.dist([df.loc[i]['широта'],df.loc[i]['долгота']],center_cluster[j])
                cluster[i] = j
        if min_dist > threshold:
            cluster[i] = len(center_cluster)
            center_cluster.append([df.loc[i]['широта'],df.loc[i]['долгота']])
    # MODIFIYING
    for i in range (df.shape[0]):
        if [df.loc[i]['широта'],df.loc[i]['долгота']] in center_cluster:
            continue
        dist = math.dist([df.loc[i]['широта'],df.loc[i]['долгота']], center_cluster[cluster[i]])
        for k in range(len(center_cluster)):
            if math.dist([df.loc[i]['широта'],df.loc[i]['долгота']],center_cluster[k]) < dist:
                dist = math.dist([df.loc[i]['широта'],df.loc[i]['долгота']],center_cluster[k])
                cluster[i] = k
    
    return cluster,center_cluster



#PLOT LOCATION
def plot_my_alg(df,target_df,signal,threshold):
    location = df[["широта","долгота"]].copy()
    label,center_cluster = my_algorithm(location,threshold)
    df["кластер"] = label
    u_labels = np.unique(label)
    label_target = predict_cluster_sobstveni(df,target_df)
    #u_target_labels = np.unique(label_target)
    target_df["кластер"] = label_target
    global m
    if signal == 0:
        plt.figure(figsize = (20,10))
        for i in u_labels:
            plt.scatter(df[label == i]["широта"] , df[label == i]["долгота"] , label = i,s = 200,edgecolors = 'black',marker = m[i])
            #ax4.scatter(center_cluster[i][0],center_cluster[i][1],c = 'black',s = 200,edgecolors = 'yellow',marker = ".")
        plt.legend()
        plt.xlabel("Широта")
        plt.ylabel("Долгота")  
        plt.title("Базовая кластеризация - Мой алгоритм")

        mplcursors.cursor().connect(
             "add", lambda sel: sel.annotation.set_text(df.loc[(df['широта']==sel.target[0]) & (df['долгота']==sel.target[1] )]["цена за кв м"].mean().astype(int))
        )
        plt.show()
    elif signal == 1:
        plt.figure(figsize = (20,10))
        for i in u_labels:
            plt.scatter(df[label == i]["широта"] , df[label == i]["долгота"] , label = i,s = 200,edgecolors = 'black',marker = m[i])
        plt.scatter(target_df["широта"],target_df["долгота"] , label = "Без оценки",c = 'black',s = 200,edgecolors = 'yellow',marker = "*")
        plt.legend()
        plt.xlabel("Широта")
        plt.ylabel("Долгота")  
        plt.title("Квартиры без оценки - Мой алгоритм")        
        mplcursors.cursor().connect(
             "add", lambda sel: sel.annotation.set_text(df.loc[(df['широта']==sel.target[0]) & (df['долгота']==sel.target[1] )]["цена за кв м"].mean().astype(int))
        )        
        plt.show()
    elif signal == 2:
        plt.figure(figsize = (20,10))
        mean_each_cluster = df.groupby(['кластер']).mean()['цена за кв м'].copy()
        target_with_mean_cluster = target_df.copy()
        for i in u_labels:
            target_with_mean_cluster.loc[target_with_mean_cluster['кластер'] == i,"цена за кв м"] = mean_each_cluster[i]
        frames = [df,target_with_mean_cluster]
        concatinated = pd.concat(frames)
        concatinated = concatinated.reset_index(drop = True)
        for i in u_labels:
            x = concatinated.loc[concatinated['кластер'] == i]["широта"]
            y = concatinated.loc[concatinated['кластер'] == i]["долгота"]
            plt.scatter( x , y, label = i,s = 200,edgecolors = 'black',marker = m[i])
        plt.legend()
        plt.xlabel("Широта")
        plt.ylabel("Долгота")  
        plt.title("Квартиры c оценкой - Мой алгоритм")        
        mplcursors.cursor().connect(
              "add", lambda sel: sel.annotation.set_text(concatinated.loc[(concatinated['широта']==sel.target[0]) & (concatinated['долгота']==sel.target[1] )]["цена за кв м"].mean().astype(int))
         )
        plt.show()
    return df,target_df

def predict_cluster_sobstveni(df,target_df):
    
    grouped_df = df.copy()
    grouped_df = grouped_df.groupby(["кластер"]).agg({"широта" : ["mean"], "долгота" : ["mean"] })
    grouped_df.columns = ["широта","долгота"]
    grouped_df = grouped_df.reset_index()
    label_target = [-1.0] * target_df.shape[0]
    for i in range(target_df.shape[0]):
        xy_not_clustered = [target_df.loc[i]["широта"],target_df.loc[i]["долгота"]]
        min_dist = 10000000000
        best_cluster = -1
        for j in range(grouped_df.shape[0]):
            center_xy_clustered = [grouped_df.loc[j]["широта"],grouped_df.loc[j]["долгота"]]
            if math.dist(xy_not_clustered,center_xy_clustered ) < min_dist:
                min_dist = math.dist(xy_not_clustered,center_xy_clustered )
                best_cluster = j
        label_target[i] = grouped_df.loc[best_cluster]["кластер"]
        
    return label_target

