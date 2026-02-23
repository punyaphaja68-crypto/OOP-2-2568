# 1. FileLogSource (อ่านไฟล์จริง)
from interfaces.data_source import ILogSource
from typing import List


class FileLogSource(ILogSource):
    def __init__(self, filepath):
        self.filepath = filepath

    def get_logs(self) -> List[str]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.readlines()
        except FileNotFoundError:
            return ["Error: File not found"]