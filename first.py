from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import os

# def scrape_weather_data(year, month):
#     url = "https://www.gismeteo.ru/diary/4618/" + str(year) + "/" + str(month) + "/"
#     headers = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41"
#     }

#     req = requests.get(url, headers=headers)
#     src = req.text

#     try:
#         with open("index.html", "w") as file:
#             file.write(src)
#     except Exception:
#         return []

#     soup = BeautifulSoup(src, "lxml")

#     try:
#         tab = soup.find("table").find("tbody").find_all("tr")
#     except Exception:
#         return []


#     data_from_table = []
#     if(month < 10):
#         moun = '0' + str(month)
#     else: moun = str(month)
#     for item in tab:
#         data_from_table_td = item.find_all('td')
#         data = data_from_table_td[0].text
#         if (len(data) == 1):
#             data = '0' + data
#         temp_morning = data_from_table_td[1].text
#         pres_morning = data_from_table_td[2].text
#         wind_morning = data_from_table_td[5].text
#         temp_evening = data_from_table_td[6].text
#         pres_evening = data_from_table_td[7].text
#         wind_evening = data_from_table_td[10].text


#         data_from_table.append(
#             {
#                 "date": str(year) + "-" + moun + "-" + data,
#                 "temp_morning": temp_morning,
#                 "pressure_morning": pres_morning,
#                 "wind_morning": wind_morning,
#                 "temp_evening": temp_evening,
#                 "pressure_evening": pres_evening,
#                 "wind_evening": wind_evening
#             }
#         )

#     return data_from_table

# def write_to_csv(data):
#     with open('dataset.csv', 'a', newline='') as csvfile:
#         file_writer = csv.writer(csvfile, delimiter=",", lineterminator="\r")
#         for item in data:
#             file_writer.writerow([
#                 item["date"],
#                 item["temp_morning"],
#                 item["pressure_morning"],
#                 item["temp_evening"],
#                 item["pressure_evening"],
#                 item["wind_evening"]
#             ])


# def split_csv_by_columns(input_file):
#     with open(input_file, 'r', newline='') as f:
#         with open('X.csv', 'a', newline='') as x_file, open('Y.csv', 'a', newline='') as y_file:
#             names = ['date', 'temp_morning', 'pressure_morning', 'wind_morning', 'temp_evening', 'pressure_evening', 'wind']
#             reader = csv.DictReader(f, fieldnames=names)

#             x_writer = csv.writer(x_file, lineterminator="\n")
#             y_writer = csv.writer(y_file, lineterminator="\n")

#             for row in reader:
#                 x_writer.writerow([row['date']])
#                 y_writer.writerow([row['temp_morning'], row['pressure_morning'], row['wind_morning'], row['temp_evening'], row['pressure_evening'], row['wind']])



def write_data_by_year(input_file):
    output_file = f'{year}.csv'
    output_folder = 'years'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, output_file)
    
    with open(input_file, newline='') as f:
        names = ['date', 'temp_morning', 'pressure_morning', 'wind_morning', 'temp_evening', 'pressure_evening', 'wind_evening']
        reader = csv.DictReader(f, fieldnames=names)
        
        with open(output_file, 'w', newline='') as file_writer:
            writer = csv.writer(file_writer, lineterminator="\n")
            for row in reader:
                year_in_row = row['date'].split('-')[0]
                if year_in_row == str(year):
                    writer.writerow([row['date'], row["temp_morning"], row["pressure_morning"], row["wind_morning"], row["temp_evening"], row["pressure_evening"], row["wind_evening"]])


def process_year_files(folder_path):
    for file_name in os.listdir(folder_path):
        input_file = os.path.join(folder_path, file_name)
        
        with open(input_file, 'r', newline='') as file:
            fieldnames = ['date', 'temp_morning', 'pressure_morning', 'wind_morning', 'temp_evening', 'pressure_evening', 'wind_evening']
            reader = csv.DictReader(file, fieldnames=fieldnames)
            try:
                first_row = next(reader)
            except StopIteration:
                file.close()
                os.remove(input_file)
                continue
            year = first_row['date'][:4]
            first_date = first_row['date'][5:7] + first_row['date'][8:10]
            last_date = None
            for row in reader:
                last_date = row['date'][5:7] + row['date'][8:10]
            if last_date is None:
                last_date = first_date
            if last_date:
                output_file = os.path.join(folder_path, f'{year}{first_date}-{year}{last_date}.csv')
                file.close()
                os.rename(input_file, output_file)




def split_csv_by_weeks(input_file):
    with open(input_file, newline='') as file:
        fieldnames = ['date', 'temp_morning', 'pressure_morning', 'wind_morning', 'temp_evening', 'pressure_evening', 'wind_evening']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        week_start = None
        week_number = 1
        week_data = []
        
        for row in reader:
            date = dt.datetime.strptime(row['date'], '%Y-%m-%d')
            day_of_week = date.weekday()

            if week_start is None:
                week_start = date - dt.timedelta(days=day_of_week)

            if day_of_week == 6:
                output_folder = 'week'
                os.makedirs(output_folder, exist_ok=True)
                output_file = os.path.join(output_folder, f'week-{week_number}.csv')

                with open(output_file, 'w', newline='') as file_writer:
                    writer = csv.writer(file_writer, lineterminator="\n")
                    for week_data_row in week_data:
                        writer.writerow(week_data_row)

                week_number += 1
                week_start = None
                week_data = []

            week_data.append([row['date'], row["temp_morning"], row["pressure_morning"], row["wind_morning"], row["temp_evening"], row["pressure_evening"], row["wind_evening"]])





    


# for year in range(1997, 2024):
#     for month in range(1, 13):
#         weather_data = scrape_weather_data(year, month)
#         write_to_csv(weather_data)
# split_csv_by_columns('dataset.csv')
for year in range(1997, 2024):
    for month in range(1, 13):
        write_data_by_year('dataset.csv')
        process_year_files('years')
        
split_csv_by_weeks('dataset.csv')