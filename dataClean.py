#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 03:13:51 2022

@author: jiahuiwu
"""
import pandas as pd
import pgeocode
import geopandas as gpd
import folium

data = pd.read_csv("out.csv")

#get company name
company_list = list(data["recipient_name"].unique())
parent_company_list = list(data["recipient_parent_name"].unique())

#get coordinate of each company

#reserve first 5 digits of the zipcode
data["zipcode"] = data["recipient_zip_4_code"].apply(lambda x: x[:5])

company_zipcode_df = pd.DataFrame(data[["recipient_name", "zipcode"]].groupby(["recipient_name", "zipcode"]).size())
company_zipcode_df.reset_index(inplace = True)


zipcode_convert = pgeocode.Nominatim('US')

def get_lat_long_by_zipcode(zipcode):
    info = zipcode_convert.query_postal_code(zipcode)
    return [info["latitude"], info["longitude"]]
    

company_zipcode_df["lat_long"] = company_zipcode_df["zipcode"].apply(get_lat_long_by_zipcode)
company_zipcode_df["lat"] = company_zipcode_df["lat_long"].apply(lambda x: x[0])
company_zipcode_df["long"] = company_zipcode_df["lat_long"].apply(lambda x: x[1])


# get sum of reward
total = data[["recipient_name", "zipcode", "potential_total_value_of_award"]].groupby(["recipient_name", "zipcode"]).sum()
total.reset_index(inplace = True)

#join two table 
company_ZC_total_df = pd.merge(company_zipcode_df, total, how = "inner", on = ["recipient_name", "zipcode"])


#get info of product

company_ZC_product_df = pd.DataFrame(data[["recipient_name", "product_or_service_code_description", "zipcode"]].groupby(["recipient_name", "product_or_service_code_description", "zipcode"]).size())
company_ZC_product_df.reset_index(inplace = True)

def get_product(company, zipcode):
    temp = company_ZC_product_df.loc[company_ZC_product_df["recipient_name"] == company, ]
    temp = temp.loc[temp["zipcode"] == zipcode, ]
    product_list  = list(temp["product_or_service_code_description"])
    allProduct = ""
    for i in product_list:
        i = i.lower()
        if(allProduct == ""):
            allProduct = i
        else:
            allProduct = allProduct + ". " + i
    return allProduct
    
test = company_ZC_total_df[["recipient_name", "zipcode"]].head()

company_ZC_total_df["product"] = company_ZC_total_df[["recipient_name", "zipcode"]].apply(lambda x: get_product(x[0], x[1]), axis = 1)

company_ZC_total_df = company_ZC_total_df.drop('lat_long', axis = 1)
company_ZC_total_df.rename({'0':"count"}, inplace = True)
company_ZC_total_df = company_ZC_total_df.drop("Unnamed: 0", axis = 1)
# company_ZC_total_df = company_ZC_total_df.drop("Unnamed: 0.1", axis = 1)


company_ZC_total_df.to_csv("company_ZC_total_df.csv", index = False)











