import csv


def divide_on_x_y(csv_file: str):
    """Divides the source file into two new ones. The first contains only dates, the second only weather data. Return None"""
    with open(csv_file, newline="") as f:
        fieldnames = [
            "date",
            "temp_morning",
            "presure_morning",
            "wind_morning",
            "temp_evening",
            "presure_evening",
            "wind",
        ]
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            file_writer = csv.writer(
                open("X.csv", "a", newline=""), lineterminator="\r"
            )
            file_writer.writerow([row["date"]])
            file_writer = csv.writer(
                open("Y.csv", "a", newline=""), lineterminator="\r"
            )
            file_writer.writerow(
                [
                    row["temp_morning"],
                    row["presure_morning"],
                    row["wind_morning"],
                    row["temp_evening"],
                    row["presure_evening"],
                    row["wind"],
                ]
            )
    return None


if __name__ == "__main__":
    divide_on_x_y("dataset.csv")
