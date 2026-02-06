from .repositories import ITaskRepository
from .models import TaskCreate

class TaskService:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def get_tasks(self):
        return self.repo.get_all()

    def create_task(self, task_in: TaskCreate):
        # Business logic เช่น การตรวจสอบคำหยาบ หรือเช็คสิทธิ์ สามารถใส่ตรงนี้ได้จ้ะ
        return self.repo.create(task_in)
    
    def mark_task_complete(self, task_id: int): # แก้ไข: ใส่ :
        # เรียกใช้ฟังก์ชัน update และส่ง task_id เข้าไปให้ Repository จ้ะ
        return self.repo.update(task_id)