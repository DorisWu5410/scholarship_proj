#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 16:15:15 2022

@author: jiahuiwu
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
from sklearn.model_selection import train_test_split
import random

company_ZC_total_df = pd.read_csv("company_ZC_total_df.csv", index_col = False)


# search product

def search_prod(name, string):
    try:
        string.index(name)
        return 1
    except:
        return 0
    
    
#find common

allprod = ""
for _, j in company_ZC_total_df.iterrows():
    allprod = allprod + str(j["product"])



allprod = re.sub('[^0-9a-zA-Z]+', ' ', allprod).split(" ")

stop_words = set(stopwords.words('english'))

allprod = [i for i in allprod if i not in stop_words]

word_count = dict(Counter(allprod))
word_count =  dict(sorted(word_count.items(), key=lambda item: item[1], reverse= True))
words = list(word_count.keys())
word_freq = list(word_count.values())



#pick some core key words and create dummy variables

def create_dummy(name):
    company_ZC_total_df[name] = company_ZC_total_df["product"].apply(lambda x: search_prod(name,x))

key_words = ["equipment", 
             "repair", 
             "defense", 
             "support", 
             "telecom", 
             "miscellaneous", 
             "professional", 
             "component", 
             "development", 
             "research", 
             "software",
             "hardware",
             "alteration",
             "maint",
             "electr",
             "management", 
             "techn",
             "aircraft",
             "medical",
             "system",
             "administrative",
             "exploratory",
             "power",
             "materials",
             "national",
             "telecommunication",
             "air",
             "vehicular",
             "wire",
             "security",
             "military", 
             "advanced",
             "measuring",
             "detection",
             "engine",
             "control",
             "specialized",
             "network",
             "energy",
             "atomic",
             "data",
             "weapon",
             "machine",
             "computing",
             "optical",
             "nuclear",
             "space"
             ]

for word in key_words:    
    create_dummy(word)





#split test train

train_idx = random.sample(range(len(company_ZC_total_df)), int(len(company_ZC_total_df) / 1.15))
train_df = company_ZC_total_df.iloc[train_idx,]

test_df = company_ZC_total_df.iloc[[i for i in range(len(company_ZC_total_df)) if i not in train_idx],]

train_df.to_csv("train_df.csv",index = False)
test_df.to_csv("test_df.csv", index = False)




#SOM
from minisom import MiniSom
import numpy as np


Input = train_df.loc[:, ~train_df.columns.isin(["recipient_name", "zipcode", "product"])]
Input["potential_total_value_of_award"] = (Input["potential_total_value_of_award"] - np.mean(Input["potential_total_value_of_award"])) / np.std(Input["potential_total_value_of_award"])

Input = Input.values
Input[np.isnan(Input)] = 0


som = MiniSom(1, 3, 49, sigma = 0.1, learning_rate = 0.5, neighborhood_function='gaussian', random_seed=10)

Input_temp = np.delete(Input, [1,2], axis = 1)
som.train(Input_temp, 500, verbose = True)

winner_coordinates = np.array([som.winner(x) for x in Input_temp]).T

cluster_index = np.ravel_multi_index(winner_coordinates, (1,3))


# import matplotlib.pyplot as plt


# plotting the clusters using the first 2 dimentions of the data
# for c in np.unique(cluster_index):
#     plt.scatter(Input[cluster_index == c, 1],
#                 Input[cluster_index == c, 2], label='cluster='+str(c), alpha=.7, s = 1)
    

train_df["cluster_index"] = cluster_index
    
def set_color(cluster):
    if cluster == 1:
        return "#8FBC8F"
    elif cluster == 0:
        return "#FFD700"
    else:
        return "#EE5C42"
        
train_df["color"] = train_df["cluster_index"].apply(set_color)


import folium
from map import Basemap

def generate_circle(df, Map):
    for _, point in df.iterrows():
        if np.isnan(point["lat"]):
            continue
        folium.CircleMarker(
            location=[point["lat"], point["long"]],
            popup = point['recipient_name'],
            color = point["color"],
            radius = 3,
            fill = True,
            fill_color=point["color"],
            fill_opacity = 1,
            icon = "circle"
            # icon = folium.Icon(icon='fa-thin fa-building')
   ).add_to(Map)

m = Basemap()
generate_circle(train_df, m)
m.save("circle_map.html")

    
    

# plotting centroids
# for centroid in som.get_weights():
#     plt.scatter(centroid[:, 0], centroid[:, 1], marker='x', 
#                 s=80, linewidths=1, color='k', label='centroid')
# plt.legend();




#result eda


import seaborn as sns
import matplotlib.pyplot as plt


box = sns.boxplot(x = train_df["cluster_index"], y = train_df["potential_total_value_of_award"])
box.set_ylim([-100000, 100000000000])



def generate_ratio(cluster):
    temp = train_df.loc[train_df["cluster_index"] == cluster,]
    ratio_list = []
    for word in key_words:
        count = sum(temp[word] == 1)
        ratio = count / len(temp)
        ratio_list.append(ratio)
    return ratio_list




fig, ax = plt.subplots(figsize = (20,8))

x = np.arange(len(key_words))

ratio_list1 = generate_ratio(0) 
rects1 = ax.bar(x + 0.3, ratio_list1, color = "#FFD700", width = 0.3, label='cluster 0')

ratio_list2 = generate_ratio(1) 
rects2 = ax.bar(x - 0.3, ratio_list2, color = "#8FBC8F", width = 0.3, label='cluster 1')

ratio_list3 = generate_ratio(2) 
rects3 = ax.bar(x, ratio_list3, color = "#EE5C42", width = 0.3, label='cluster 2')

ax.legend()

ax.set_xticks(np.arange(len(key_words)))
ax.set_xticklabels(key_words)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
ax.set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])

ax.set_xlabel('product', labelpad=15, size = 13)
ax.set_ylabel('proportion in each cluster', labelpad=15, size = 13)
ax.set_title('Ratio distribution of product for each cluster', pad=15, size = 13)

plt.xticks(fontsize = 11, rotation = 75)
plt.yticks(fontsize = 11)














