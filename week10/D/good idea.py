from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        print("Saving data to MySQL database...")
    
class PostgreSQLDatabase(Database):
    def save(self, data):
        print("Saving data to PostgreSQL database...")

class App:
    def __init__(self, db: Database):
        self.database = db  # ใช้ db ที่ถูกส่งเข้ามาแทนที่ MySQLDatabase() โดยตรง
    def save_data(self, data):
        self.database.save(data)
      