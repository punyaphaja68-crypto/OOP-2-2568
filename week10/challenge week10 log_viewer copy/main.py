import os
from PySide6.QtWidgets import QApplication
from services.mock_source import MockLogSource
from services.log_factory import LogFactory
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "logs", "voters.csv")
    # เปลี่ยนไฟล์ voters.log / voters.csv

    use_mock = False

    if use_mock:
        log = MockLogSource()
    else:
        log = LogFactory.create_source(file_path)

    viewer = MainWindow(log)
    viewer.show()

    app.exec()