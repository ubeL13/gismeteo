
from bs4 import BeautifulSoup
import requests
import csv
import os
import datetime as dt

years = list(range(1997, 2024))
months = list(range(1, 13))

def get_url(year, month):
    return "https://www.gismeteo.ru/diary/4618/" + str(year) + "/" + str(month) + "/"

def get_headers():
    return { 
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41" 
        }

def get_data_from_table(tab, year, month):
    data_from_table = [] 
    if(month < 10): 
        moun = '0' + str(month) 
    else: moun = str(month) 
    for item in tab: 
        data_from_table_td = item.find_all('td') 
        data = data_from_table_td[0].text 
        if (len(data) == 1): 
            data = '0' + data 
        temp_morning = data_from_table_td[1].text 
        pres_morning = data_from_table_td[2].text 
        wind_morning = data_from_table_td[5].text 
        temp_evening = data_from_table_td[6].text 
        pres_evening = data_from_table_td[7].text 
        wind_evening = data_from_table_td[10].text 

        data_from_table.append( 
            { 
                "data": str(year) + "-" + moun + "-" + data, 
                "temp_morning": temp_morning, 
                "presure_morning": pres_morning, 
                "wind_morning": wind_morning, 
                "temp_evening": temp_evening, 
                "presure_evening": pres_evening, 
                "wind_evening": wind_evening 
            } 
        ) 

    return data_from_table



for year in years: 
    for month in months:
        url = get_url(year, month)
        headers = get_headers()
        req = requests.get(url, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml") 
        try: 
            tab = soup.find("table").find("tbody").find_all("tr") 
        except Exception: 
            continue

        data_from_table = get_data_from_table(tab, year, month)
        


