from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    studentId: str
