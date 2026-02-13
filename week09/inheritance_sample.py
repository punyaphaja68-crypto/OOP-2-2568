class Student:
    def __init__(self,pid,name,age,student_id):
        self.name = name
        self.pid = pid
        self.age = age
class Staff:
    def __init__(self,pid,name,age,staff_id):
        self.pid = pid
        self.name
        self.age

class Person:
    def __init_(self):
       self.pid
       self.name
       self.age
    def __str__(self):
       return f"Name: {self.name} , Age: {self.age}"     

class Student(Person):
    def __init__(self,pid ,name,age,student_id):
     super().__init__(pid,name,age)
     self.student_id = student_id

class Staff(Person):
    def __init__(self,pid ,name,age,staff_id):
     super().__init__(pid,name,age)
     self.staff = staff_id

person = Person("1111111112" ,"John",30)
student = Student(112222222111,"Alice",20,"S123")
staff = Staff(1111111111111,"Bob",35,"ST456")
print(f"Student: {student.name} ,Age {student.age} , Student_id {student.student_id}")
print(f"Staff: {staff.name} ,Aage {staff.age} ,Staff_id {staff.staff_id}")

def get_person_info(Person):
   print(isinstance)