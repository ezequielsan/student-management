from .student import Student

class PostGraduateStudent(Student):
    thesisTitle: str
    supervisor: str
    workedDays: int
    scholarshipAmount: float
