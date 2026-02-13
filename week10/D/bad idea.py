class App:
    def __init__(self, db):
        self.database = db  # ใช้ db ที่ถูกส่งเข้ามาแทนที่ MySQLDatabase() โดยตรง
    def save_data(self, data):
        self.database.save(data)

class MySQLDatabase:
    def save(self, data):
        print("Saving data to MySQL database...")

app = App()
app.save_data("Some important data")