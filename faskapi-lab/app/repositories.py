from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Task, TaskCreate
from . import models_orm

class ITaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def create(self, task: TaskCreate) -> Task:
        pass
        
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def update(self, task_id: int) -> Optional[Task]: # แก้ไข: ใส่ : และตั้งชื่อให้กลางๆ
        pass

class InMemoryTaskRepository(ITaskRepository):
    def __init__(self):
        self.tasks = []
        self.current_id = 1

    def get_all(self) -> List[Task]:
        return self.tasks

    def create(self, task_in: TaskCreate) -> Task:
        task = Task(id=self.current_id, **task_in.dict())
        self.tasks.append(task)
        self.current_id += 1
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task_id: int) -> Optional[Task]: # เพิ่มให้ครบตาม Interface
        task = self.get_by_id(task_id)
        if task:
            task.completed = True # สมมติว่าเป็นการ update สถานะ
        return task

class SqlTaskRepository(ITaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Task]:
        return self.db.query(models_orm.Task).all()

    def create(self, task_in: TaskCreate) -> Task:
        db_task = models_orm.Task(**task_in.dict())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task
    
    def update(self, task_id: int) -> Optional[Task]: # แก้ไข: ชื่อต้องตรงกับ ITaskRepository
        db_task = self.get_by_id(task_id)
        if db_task:
            db_task.completed = True
            self.db.commit()
            self.db.refresh(db_task)
        return db_task

    def get_by_id(self, task_id: int) -> Optional[Task]: # แก้ไข: ชื่อตัวแปร และใส่ .first()
        return self.db.query(models_orm.Task).filter(models_orm.Task.id == task_id).first()