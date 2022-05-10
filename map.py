#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 13:15:06 2022

@author: jiahuiwu
"""
import pandas as pd
import geopandas as gpd
import folium
import numpy as np



company_ZC_total_df = pd.read_csv("company_ZC_total_df.csv")

USA = gpd.read_file("geoBoundaries-USA-ADM1_simplified.geojson")

def Basemap():
    map1 = folium.Map(zoom_start = 4,location=[44.8926, -100.0753], tiles='cartodbpositron',max_bounds=True, min_zoom = 4, max_zoom = 10)
    
    allparts = [p.buffer(0) for p in USA["geometry"]]
    names = [p for p in USA["shapeName"]]
    
    for i in range(len(allparts)):
        name = names[i]
        r = allparts[i]
        sim_geo = gpd.GeoSeries(r).simplify(tolerance = 0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': '#FFE6EE','color':'gray','weight':1.5})
        folium.Popup(name).add_to(geo_j)
        geo_j.add_to(map1)
        
    return(map1)

m = Basemap()
m.save("basemap.html")




#draw top 1000 with largest reward amount
company_ZC_total_df = company_ZC_total_df.sort_values(by = ["potential_total_value_of_award"], ascending = False)
company_ZC_total_df.reset_index(inplace = True)

def generate_marker(df, Map):
    for _, point in df.iloc[:500,].iterrows():
        if np.isnan(point["lat"]):
            continue
        folium.Marker(
            location=[point["lat"], point["long"]],
            popup = point['recipient_name'],
            # icon = folium.Icon(icon='fa-thin fa-building')
   ).add_to(Map)
        
m = Basemap() 
generate_marker(company_ZC_total_df, m)
m.save("test.html")



