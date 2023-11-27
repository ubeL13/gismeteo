from bs4 import BeautifulSoup
import requests
import csv
import os;

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
        data = data_from_table_td[0].text
        temp_morning = data_from_table_td[1].text
        pres_morning = data_from_table_td[2].text
        wind_morning = data_from_table_td[5].text
        temp_evening = data_from_table_td[6].text
        pres_evening = data_from_table_td[7].text
        wind_evening = data_from_table_td[10].text

        data_from_table.append(
            {
                "data": f"{data}.{month}.{year}",
                "temp_morning": temp_morning,
                "presure_morning": pres_morning,
                "wind_morning": wind_morning,
                "temp_evening": temp_evening,
                "presure_evening": pres_evening,
                "wind_evening": wind_evening
            }
        )

    return data_from_table

def write_to_csv(data):
    with open('dataset.csv', 'a', newline='') as csvfile:
        file_writer = csv.writer(csvfile, delimiter=",", lineterminator="\r")
        for item in data:
            file_writer.writerow([
                item["data"],
                item["temp_morning"],
                item["presure_morning"],
                item["temp_evening"],
                item["presure_evening"],
                item["wind_evening"]
            ])


def split_csv(data, output_file_x, output_file_y):
    with open('dataset.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Определение количества строк
    num_rows = len(rows)
    half_rows = num_rows // 2

    # Разбивка на два списка
    x_rows = rows[:half_rows]
    y_rows = rows[half_rows:]

    # Запись в файлы X.csv и Y.csv
    with open(output_file_x, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(x_rows)

    with open(output_file_y, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(y_rows)

# Пример использования






for year in range(1997, 2024):
    for month in range(1, 13):
        weather_data = scrape_weather_data(year, month)
        write_to_csv(weather_data)
        split_csv('dataset.csv', 'X.csv', 'Y.csv')