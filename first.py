
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

def write_to_csv(data_from_table):
    with open('dataset.csv', 'a', newline='') as csvfile: 
        for item in data_from_table: 
            file_writer = csv.writer(csvfile, delimiter=",", lineterminator="\r") 
            file_writer.writerow([item["data"], item["temp_morning"], item["presure_morning"], item["wind_morning"], item["temp_evening"], item["presure_evening"], item["wind_evening"]]) 

def read_csv_and_write_to_new_files():
    with open('dataset.csv', newline='') as f: 
        fieldnames = ['data', 'temp_morning', 'presure_morning', 'wind_morning', 'temp_evening', 'presure_evening', 'wind'] 
        reader = csv.DictReader(f, fieldnames=fieldnames) 
        for row in reader: 
            file_writer = csv.writer(open('dataset-number.csv', 'a', newline=''), lineterminator="\r") 
            file_writer.writerow([row['data']]) 
            file_writer = csv.writer(open('dataset-meteodate.csv', 'a', newline=''), lineterminator="\r") 
            file_writer.writerow([row['temp_morning'], row['presure_morning'], row['wind_morning'], row['temp_evening'], row['presure_evening'], row['wind']]) 

for year in years: 
    for month in months:
        url = get_url(year, month)
        headers = get_headers()
        req = requests.get(url, headers=headers)
        src = req.text
        try: 
            with open("cite.html", "w") as file: 
                file.write(src) 
        except Exception: 
            continue

        soup = BeautifulSoup(src, "lxml") 
        try: 
            tab = soup.find("table").find("tbody").find_all("tr") 
        except Exception: 
            continue

        data_from_table = get_data_from_table(tab, year, month)
        write_to_csv(data_from_table)

read_csv_and_write_to_new_files()

