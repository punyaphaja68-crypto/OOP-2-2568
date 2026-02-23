import csv
from interfaces.data_source import ILogSource


class CsvLogSource(ILogSource):
    def __init__(self, filename):
        self.filename = filename

    def get_logs(self):
        formatted_logs = []

        with open(self.filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                log_line = (
                    f"Name: {row['ชื่อ']}  |  "
                    f"Age: {row['อายุ']}  |  "
                    f"Province: {row['จังหวัด']}  |  "
                    f"Party: {row['พรรคที่เลือก']}"
                )
                formatted_logs.append(log_line)

        return "\n".join(formatted_logs)