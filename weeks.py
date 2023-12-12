import csv
import os
import datetime as dt
def divide_by_week(csv_file):
    with open(csv_file, newline='') as file:
        fieldnames = ['data', 'temp_morning', 'presure_morning', 'wind_morning', 'temp_evening', 'presure_evening',
                  'wind_evening']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        week_start = None
        week_number = 1
        week_data = []
        for row in reader:
            date = dt.datetime.strptime(row['data'], '%Y-%m-%d')
            day_of_week = date.weekday()
            if(row['data'][:4] == '1998' or row['data'][:4] == '2000'):
                week_data.append(
                    [row['data'], row["temp_morning"], row["presure_morning"], row["wind_morning"], row["temp_evening"],
                    row["presure_evening"], row["wind_evening"]])
                output_folder = 'week'
                os.makedirs(output_folder, exist_ok=True)
                output_file = os.path.join(output_folder, f'week-{week_number}.csv')

                with open(output_file, 'w', newline='') as file_writer:
                    writer = csv.writer(file_writer, lineterminator="\r")
                    for week_data in week_data:
                        writer.writerow(week_data)

                week_number += 1
                week_start = None
                week_data = []
                continue

            if week_start is None:
                week_start = date - dt.timedelta(days=day_of_week)

            if day_of_week == 6:
                output_folder = 'week'
                os.makedirs(output_folder, exist_ok=True)
                output_file = os.path.join(output_folder, f'week-{week_number}.csv')

                with open(output_file, 'w', newline='') as file_writer:
                    writer = csv.writer(file_writer, lineterminator="\r")
                    for week_data in week_data:
                        writer.writerow(week_data)

                week_number += 1
                week_start = None
                week_data = []

            week_data.append(
                [row['data'], row["temp_morning"], row["presure_morning"], row["wind_morning"], row["temp_evening"],
                row["presure_evening"], row["wind_evening"]])
    return None


if __name__ == '__main__':
    divide_by_week('dataset.csv')
