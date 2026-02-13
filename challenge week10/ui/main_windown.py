from inter 

class mainWindown(QMainwindown):
    def __init__(self):
        super().__init__()
        self.log_source = log_source
        self.load_logs()
        self.centerWindowTitle(self.log_source.get_display_name())
        self.display.setReadOnly(True)
        self.init_ui()

    def load_logs(self):
        logs = self.log_source.get_logs()
        for log in logs:
            self.log_listbox.insert(END, log)