from PySide6.QtWidgets import *
from interfaces.data_source import ILogSource


class MainWindow(QMainWindow):

    def __init__(self, log_source: ILogSource):
        super().__init__()

        self.log_display = QTextEdit(self)
        self.resize(800, 600)
        self.setCentralWidget(self.log_display)
        self.log_display.setReadOnly(True)

        self.log_source = log_source

        self.load_logs()  # ตอนนี้จะไม่ error แล้ว
        self.show()

    def load_logs(self):
        logs = self.log_source.get_logs()
        self.log_display.setText(logs)