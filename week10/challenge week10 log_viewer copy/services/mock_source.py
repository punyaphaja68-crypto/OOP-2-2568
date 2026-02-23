# 2. MockLogSource (ข้อมูลจำลอง)
from interfaces.data_source import ILogSource
from typing import List


class MockLogSource(ILogSource):
    def get_logs(self) -> List[str]:
        return [
            "[INFO] System started",
            "[WARN] Memory usage high",
            "[ERROR] Connection lost",
        ]