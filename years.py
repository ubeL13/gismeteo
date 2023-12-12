import csv
import os


def divide_by_years(csv_file: str):
    """Divide the source csv_file by years. Return None"""
    for year in range(1997, 2024):
        output_file = f"{year}.csv"
        output_folder = "years"
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, output_file)
        with open(csv_file, newline="") as f:
            fieldnames = [
                "data",
                "temp_morning",
                "presure_morning",
                "wind_morning",
                "temp_evening",
                "presure_evening",
                "wind_evening",
            ]
            reader = csv.DictReader(f, fieldnames=fieldnames)
            with open(output_file, "w", newline="") as file_writer:
                writer = csv.writer(file_writer, lineterminator="\r")
                for row in reader:
                    year_in_row = row["data"].split("-")[0]
                    if year_in_row == str(year):
                        writer.writerow(
                            [
                                row["data"],
                                row["temp_morning"],
                                row["presure_morning"],
                                row["wind_morning"],
                                row["temp_evening"],
                                row["presure_evening"],
                                row["wind_evening"],
                            ]
                        )

    for year in range(1997, 2024):
        input_file = f"years/{year}.csv"
        with open(input_file, "r", newline="") as file:
            fieldnames = [
                "data",
                "temp_morning",
                "presure_morning",
                "wind_morning",
                "temp_evening",
                "presure_evening",
                "wind_evening",
            ]
            reader = csv.DictReader(file, fieldnames=fieldnames)
            try:
                first_row = next(reader)
            except Exception:
                file.close()
                os.remove(input_file)
                continue
            year = first_row["data"][:4]
            first_date = first_row["data"][5:7] + first_row["data"][8:10]
            last_date = None
            for row in reader:
                last_date = row["data"][5:7] + row["data"][8:10]
            if last_date is None:
                last_date = first_date
            if last_date:
                output_file = f"years/{year}{first_date}-{year}{last_date}.csv"
                file.close()
                os.rename(input_file, output_file)
    return None


if __name__ == "__main__":
    divide_by_years("dataset.csv")
