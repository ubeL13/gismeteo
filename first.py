from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime, timedelta
import os

def scrape_weather_data(year, month):
    url = "https://www.gismeteo.ru/diary/4618/" + str(year) + "/" + str(month) + "/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41"
    }

    req = requests.get(url, headers=headers)
    src = req.text

    try:
        with open("index.html", "w") as file:
            file.write(src)
    except Exception:
        return []

    soup = BeautifulSoup(src, "lxml")

    try:
        tab = soup.find("table").find("tbody").find_all("tr")
    except Exception:
        return []

    data_from_table = []
    for item in tab:
        data_from_table_td = item.find_all('td')
        date = data_from_table_td[0].text
        temp_morning = data_from_table_td[1].text
        pres_morning = data_from_table_td[2].text
        wind_morning = data_from_table_td[5].text
        temp_evening = data_from_table_td[6].text
        pres_evening = data_from_table_td[7].text
        wind_evening = data_from_table_td[10].text

        data_from_table.append(
            {
                "date": f"{date}.{month}.{year}",
                "temp_morning": temp_morning,
                "pressure_morning": pres_morning,
                "wind_morning": wind_morning,
                "temp_evening": temp_evening,
                "pressure_evening": pres_evening,
                "wind_evening": wind_evening
            }
        )

    return data_from_table

def write_to_csv(data):
    with open('dataset.csv', 'a', newline='') as csvfile:
        file_writer = csv.writer(csvfile, delimiter=",", lineterminator="\r")
        for item in data:
            file_writer.writerow([
                item["date"],
                item["temp_morning"],
                item["pressure_morning"],
                item["temp_evening"],
                item["pressure_evening"],
                item["wind_evening"]
            ])

        

#######
# with open('dataset.csv', newline='') as f:
#     fieldnames = ['data', 'temp_morning', 'presure_morning', 'wind_morning', 'temp_evening', 'presure_evening', 'wind']
#     reader = csv.DictReader(f, fieldnames=fieldnames)
#     for row in reader:
#         file_writer = csv.writer(open('X.csv', 'a', newline=''), lineterminator="\r")
#         file_writer.writerow([row['data']                  ])
#         file_writer = csv.writer(open('Y.csv', 'a', newline=''), lineterminator="\r")
#         file_writer.writerow([row['temp_morning'], row['presure_morning'], row['wind_morning'], row['temp_evening'], row['presure_evening'], row['wind']])
# ####

with open('dataset.csv', newline='') as f:
    with open('X.csv', 'a', newline='') as x_file, open('Y.csv', 'a', newline='') as y_file:
        names = ['date', 'temp_morning', 'pressure_morning', 'wind_morning', 'temp_evening', 'pressure_evening', 'wind']
        reader = csv.DictReader(f, fieldnames=names)

        x_writer = csv.writer(x_file, lineterminator="\r")
        y_writer = csv.writer(y_file, lineterminator="\r")

        for row in reader:
            x_writer.writerow([row['date']])
            y_writer.writerow([row['temp_morning'], row['pressure_morning'], row['wind_morning'], row['temp_evening'], row['pressure_evening'], row['wind']])


for year in range(1997, 2024):
    for month in range(1, 13):
        weather_data = scrape_weather_data(year, month)
        write_to_csv(weather_data)
       