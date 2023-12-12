# -*- coding: utf-8 -*-
import csv


def get_date_from_file(target_date: str, csvfile: str):
    """Returns data from the file by the transmitted date"""
    with open(csvfile, newline="") as f:
        fieldnames = [
            "date",
            "temp_morning",
            "presure_morning",
            "wind_morning",
            "temp_evening",
            "presure_evening",
            "wind_evening",
        ]
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            date = row["date"]
            if date == target_date:
                return {
                    "date": row["date"],
                    "temp_morning": row["temp_morning"],
                    "presure_morning": row["presure_morning"],
                    "wind_morning": row["wind_morning"],
                    "temp_evening": row["temp_evening"],
                    "presure_evening": row["presure_evening"],
                    "wind_evening": row["wind_evening"],
                }
    return None


if __name__ == "__main__":
    csvfile = "dataset.csv"
    target_date = "2013-07-07"
    date = get_date_from_file(target_date, csvfile)
    if date is None:
        print("Data is not exsist")
    if date:
        print("Data is:")
        for i, j in date.items():
            print(i)
            j = j.encode('WINDOWS_1251')
            print(j.decode('UTF-8'))
