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


m = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o',
    '^', '^', '^', '^', '^', '^', '^','^', '^',
    's', 's', 's', 's', 's', 's', 's', 's', 's',
    'D', 'D', 'D', 'D', 'D', 'D', 'D','D', 'D',
    'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
    'p','p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
    'v', 'v', 'v', 'v', 'v', 'v', 'v','v', 'v',
    ]

def plot_location_dbscan(df,target_df,signal,epsilon):
    location = df[["широта","долгота"]].copy()
    dbscan = DBSCAN(eps = epsilon, min_samples=1)
    label = dbscan.fit_predict(location)
    df["кластер"] = label
    u_labels = np.unique(label)
    label_target = predict_cluster_dbscan(df,epsilon,target_df)
    u_target_labels = np.unique(label_target)
    target_df["кластер"] = label_target
    global m
    if signal == 0:
        plt.figure(figsize = (20,10))
        for i in u_labels:
            plt.scatter(df[label == i]["широта"] , df[label == i]["долгота"] , label = i,s = 200,edgecolors = 'black',marker = m[i])
        plt.legend()
        plt.xlabel("Широта")
        plt.ylabel("Долгота")  
        plt.title("Базовая кластеризация - DBSCAN")
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
        plt.title("Квартиры без оценки - DBSCAN")
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
        plt.title("Квартиры c оценкой - DBSCAN")
        mplcursors.cursor().connect(
              "add", lambda sel: sel.annotation.set_text(concatinated.loc[(concatinated['широта']==sel.target[0]) & (concatinated['долгота']==sel.target[1] )]["цена за кв м"].mean().astype(int))
         )
        plt.show()
    return df,target_df


def predict_cluster_dbscan(df,threshold,target_df):
    label_target = [-1.0] * target_df.shape[0]
    for i in range(target_df.shape[0]):
        xy_not_clustered = [target_df.loc[i]["широта"],target_df.loc[i]["долгота"]]
        for j in range(df.shape[0]):
            xy_clustered = [df.loc[j]["широта"],df.loc[j]["долгота"]]
            if math.dist(xy_not_clustered,xy_clustered ) < threshold and (df.loc[j]["кластер"] != -1.0):
                label_target[i] = df.loc[j]["кластер"]
                break
    grouped_df = df.copy()
    grouped_df = grouped_df.groupby(["кластер"]).agg({"широта" : ["mean"], "долгота" : ["mean"] })
    grouped_df.columns = ["широта","долгота"]
    grouped_df = grouped_df.reset_index()
    for k in range(target_df.shape[0]):
        if label_target[k] == -1.0:
            xy_not_clustered = [target_df.loc[k]["широта"],target_df.loc[k]["долгота"]]
            min_dist = 10000000000
            for p in range(grouped_df.shape[0]):
                center_xy_clustered = [grouped_df.loc[p]["широта"],grouped_df.loc[p]["долгота"]]
                if math.dist(xy_not_clustered,center_xy_clustered ) < min_dist:
                    min_dist = math.dist(xy_not_clustered,center_xy_clustered )
                    label_target[k] = p
    return label_target
