import csv


class Iterator:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self._iter = self.generator()

    def generator(self):
        """Generate the iterator"""
        with open(self.csv_file, newline="") as f:
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
            for row in reader:
                date = row["data"]
                data = {
                    "data": date,
                    "temp_morning": row["temp_morning"],
                    "presure_morning": row["presure_morning"],
                    "wind_morning": row["wind_morning"],
                    "temp_evening": row["temp_evening"],
                    "presure_evening": row["presure_evening"],
                    "wind_evening": row["wind_evening"],
                }
                yield data

    def __iter__(self):
        return self

    def __next__(self):
        """Get the next date in file"""
        try:
            return next(self._iter)
        except StopIteration:
            raise StopIteration


if __name__ == "__main__":
    csv_file = "dataset.csv"
    _iter = Iterator(csv_file)
    next_data = _iter.__next__()
    print(next_data)
    next_data = _iter.__next__()
    print(next_data)
    next_data = _iter.__next__()
    print(next_data)
    next_data = _iter.__next__()
    print(next_data)
