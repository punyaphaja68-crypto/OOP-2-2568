from services.file_source import FileLogSource
from services.csv_source import CsvLogSource


class LogFactory:
    @staticmethod
    def create_source(filename):
        filename = filename.lower()

        if filename.endswith(".csv"):
            return CsvLogSource(filename)

        elif filename.endswith(".log"):
            return FileLogSource(filename)

        else:
            raise ValueError("Unsupported file type")