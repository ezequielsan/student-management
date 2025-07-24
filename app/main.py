from fastapi import FastAPI, HTTPException, Body
from app.model.student import Student
from app.model.undergraduate_student import UndergraduateStudent
from app.model.scientific_initiation_student import ScientificInitiationStudent
from app.model.post_graduate_student import PostGraduateStudent
from app.services import CSVService
from typing import List
import os

app = FastAPI(
    title="Student Management API",
    description="API para gerenciamento de estudantes, com exemplos de uso em cada endpoint.",
    version="1.0.0"
)

# CSV file paths
data_dir = os.path.join(os.path.dirname(__file__), '../data')
os.makedirs(data_dir, exist_ok=True)

student_service = CSVService(
    os.path.join(data_dir, 'students.csv'),
    Student,
    ['name', 'age', 'studentId']
)
undergrad_service = CSVService(
    os.path.join(data_dir, 'undergraduates.csv'),
    UndergraduateStudent,
    ['name', 'age', 'studentId', 'major']
)
scientific_service = CSVService(
    os.path.join(data_dir, 'scientifics.csv'),
    ScientificInitiationStudent,
    ['name', 'age', 'studentId', 'major', 'workedDays', 'scholarshipAmount']
)
postgrad_service = CSVService(
    os.path.join(data_dir, 'postgraduates.csv'),
    PostGraduateStudent,
    ['name', 'age', 'studentId', 'thesisTitle', 'supervisor', 'workedDays', 'scholarshipAmount']
)

# CRUD for Student
@app.post('/students/', response_model=Student, summary="Criar estudante", description="Cria um novo estudante. O campo studentId deve ser único.",
          response_description="Estudante criado com sucesso.",
          tags=["Student"],
          )
def create_student(student: Student):
    """Exemplo de body:
    {
      "name": "João Silva",
      "age": 20,
      "studentId": "S123"
    }
    """
    if not student.name or not student.studentId:
        raise HTTPException(status_code=422, detail='Nome e studentId são obrigatórios')
    if student.age < 0:
        raise HTTPException(status_code=422, detail='Idade não pode ser negativa')
    if student_service.get(student.studentId):
        raise HTTPException(status_code=400, detail='Student already exists')
    student_service.add(student)
    return student

@app.post('/students/batch', response_model=List[Student], summary="Criar estudantes em lote", tags=["Student"])
def create_students_batch(students: List[Student] = Body(...)):
    """Cria vários estudantes de uma vez. Exemplo de body:
    [
      {"name": "João Silva", "age": 20, "studentId": "S123"},
      {"name": "Maria Souza", "age": 21, "studentId": "S124"}
    ]
    """
    created = []
    ids = set()
    for student in students:
        if not student.name or not student.studentId:
            raise HTTPException(status_code=422, detail='Nome e studentId são obrigatórios para todos os estudantes')
        if student.age < 0:
            raise HTTPException(status_code=422, detail='Idade não pode ser negativa para todos os estudantes')
        if student.studentId in ids:
            raise HTTPException(status_code=400, detail=f'Duplicidade de studentId no batch: {student.studentId}')
        if student_service.get(student.studentId):
            raise HTTPException(status_code=400, detail=f'Student já existe: {student.studentId}')
        ids.add(student.studentId)
        student_service.add(student)
        created.append(student)
    return created

@app.get('/students/', response_model=List[Student], summary="Listar estudantes", tags=["Student"])
def list_students():
    """Retorna todos os estudantes cadastrados."""
    return student_service.read_all()

@app.get('/students/{studentId}', response_model=Student, summary="Buscar estudante", tags=["Student"])
def get_student(studentId: str):
    """Busca um estudante pelo studentId."""
    student = student_service.get(studentId)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    return student

@app.put('/students/{studentId}', response_model=Student, summary="Atualizar estudante", tags=["Student"])
def update_student(studentId: str, student: Student):
    """Atualiza os dados de um estudante pelo studentId."""
    if not student_service.get(studentId):
        raise HTTPException(status_code=404, detail='Student not found')
    student_service.update(studentId, student)
    return student

@app.delete('/students/{studentId}', summary="Remover estudante", tags=["Student"])
def delete_student(studentId: str):
    """Remove um estudante pelo studentId."""
    if not student_service.get(studentId):
        raise HTTPException(status_code=404, detail='Student not found')
    student_service.delete(studentId)
    return {'ok': True}

# CRUD for UndergraduateStudent
@app.post('/undergraduates/', response_model=UndergraduateStudent, summary="Criar undergraduate", tags=["UndergraduateStudent"])
def create_undergraduate(student: UndergraduateStudent):
    """Exemplo de body:
    {
      "name": "Maria Souza",
      "age": 21,
      "studentId": "U456",
      "major": "Engenharia"
    }
    """
    if not student.name or not student.studentId or not student.major:
        raise HTTPException(status_code=422, detail='Nome, studentId e major são obrigatórios')
    if student.age < 0:
        raise HTTPException(status_code=422, detail='Idade não pode ser negativa')
    if undergrad_service.get(student.studentId):
        raise HTTPException(status_code=400, detail='Undergraduate already exists')
    undergrad_service.add(student)
    return student

@app.post('/undergraduates/batch', response_model=List[UndergraduateStudent], summary="Criar undergraduates em lote", tags=["UndergraduateStudent"])
def create_undergraduates_batch(students: List[UndergraduateStudent] = Body(...)):
    """Cria vários undergraduates de uma vez. Exemplo de body:
    [
      {"name": "Maria Souza", "age": 21, "studentId": "U456", "major": "Engenharia"},
      {"name": "Pedro Lima", "age": 22, "studentId": "U457", "major": "Matemática"}
    ]
    """
    created = []
    ids = set()
    for student in students:
        if not student.name or not student.studentId or not student.major:
            raise HTTPException(status_code=422, detail='Nome, studentId e major são obrigatórios para todos os undergraduates')
        if student.age < 0:
            raise HTTPException(status_code=422, detail='Idade não pode ser negativa para todos os undergraduates')
        if student.studentId in ids:
            raise HTTPException(status_code=400, detail=f'Duplicidade de studentId no batch: {student.studentId}')
        if undergrad_service.get(student.studentId):
            raise HTTPException(status_code=400, detail=f'Undergraduate já existe: {student.studentId}')
        ids.add(student.studentId)
        undergrad_service.add(student)
        created.append(student)
    return created

@app.get('/undergraduates/', response_model=List[UndergraduateStudent], summary="Listar undergraduates", tags=["UndergraduateStudent"])
def list_undergraduates():
    return undergrad_service.read_all()

@app.get('/undergraduates/{studentId}', response_model=UndergraduateStudent, summary="Buscar undergraduate", tags=["UndergraduateStudent"])
def get_undergraduate(studentId: str):
    student = undergrad_service.get(studentId)
    if not student:
        raise HTTPException(status_code=404, detail='Undergraduate not found')
    return student

@app.put('/undergraduates/{studentId}', response_model=UndergraduateStudent, summary="Atualizar undergraduate", tags=["UndergraduateStudent"])
def update_undergraduate(studentId: str, student: UndergraduateStudent):
    if not undergrad_service.get(studentId):
        raise HTTPException(status_code=404, detail='Undergraduate not found')
    undergrad_service.update(studentId, student)
    return student

@app.delete('/undergraduates/{studentId}', summary="Remover undergraduate", tags=["UndergraduateStudent"])
def delete_undergraduate(studentId: str):
    if not undergrad_service.get(studentId):
        raise HTTPException(status_code=404, detail='Undergraduate not found')
    undergrad_service.delete(studentId)
    return {'ok': True}

# CRUD for ScientificInitiationStudent
@app.post('/scientifics/', response_model=ScientificInitiationStudent, summary="Criar scientific initiation student", tags=["ScientificInitiationStudent"])
def create_scientific(student: ScientificInitiationStudent):
    """Exemplo de body:
    {
      "name": "Carlos Lima",
      "age": 22,
      "studentId": "SI789",
      "major": "Computação",
      "workedDays": 120,
      "scholarshipAmount": 800.0
    }
    """
    if not student.name or not student.studentId or not student.major:
        raise HTTPException(status_code=422, detail='Nome, studentId e major são obrigatórios')
    if student.age < 0 or student.workedDays < 0:
        raise HTTPException(status_code=422, detail='Idade e workedDays não podem ser negativas')
    if student.scholarshipAmount < 0:
        raise HTTPException(status_code=422, detail='scholarshipAmount não pode ser negativo')
    if scientific_service.get(student.studentId):
        raise HTTPException(status_code=400, detail='Scientific Initiation Student already exists')
    scientific_service.add(student)
    return student

@app.post('/scientifics/batch', response_model=List[ScientificInitiationStudent], summary="Criar scientific initiation students em lote", tags=["ScientificInitiationStudent"])
def create_scientifics_batch(students: List[ScientificInitiationStudent] = Body(...)):
    """Cria vários scientific initiation students de uma vez. Exemplo de body:
    [
      {"name": "Carlos Lima", "age": 22, "studentId": "SI789", "major": "Computação", "workedDays": 120, "scholarshipAmount": 800.0},
      {"name": "Julia Alves", "age": 23, "studentId": "SI790", "major": "Física", "workedDays": 100, "scholarshipAmount": 700.0}
    ]
    """
    created = []
    ids = set()
    for student in students:
        if not student.name or not student.studentId or not student.major:
            raise HTTPException(status_code=422, detail='Nome, studentId e major são obrigatórios para todos os scientifics')
        if student.age < 0 or student.workedDays < 0:
            raise HTTPException(status_code=422, detail='Idade e workedDays não podem ser negativos para todos os scientifics')
        if student.scholarshipAmount < 0:
            raise HTTPException(status_code=422, detail='scholarshipAmount não pode ser negativo para todos os scientifics')
        if student.studentId in ids:
            raise HTTPException(status_code=400, detail=f'Duplicidade de studentId no batch: {student.studentId}')
        if scientific_service.get(student.studentId):
            raise HTTPException(status_code=400, detail=f'Scientific já existe: {student.studentId}')
        ids.add(student.studentId)
        scientific_service.add(student)
        created.append(student)
    return created

@app.get('/scientifics/', response_model=List[ScientificInitiationStudent], summary="Listar scientific initiation students", tags=["ScientificInitiationStudent"])
def list_scientifics():
    return scientific_service.read_all()

@app.get('/scientifics/{studentId}', response_model=ScientificInitiationStudent, summary="Buscar scientific initiation student", tags=["ScientificInitiationStudent"])
def get_scientific(studentId: str):
    student = scientific_service.get(studentId)
    if not student:
        raise HTTPException(status_code=404, detail='Scientific Initiation Student not found')
    return student

@app.put('/scientifics/{studentId}', response_model=ScientificInitiationStudent, summary="Atualizar scientific initiation student", tags=["ScientificInitiationStudent"])
def update_scientific(studentId: str, student: ScientificInitiationStudent):
    if not scientific_service.get(studentId):
        raise HTTPException(status_code=404, detail='Scientific Initiation Student not found')
    scientific_service.update(studentId, student)
    return student

@app.delete('/scientifics/{studentId}', summary="Remover scientific initiation student", tags=["ScientificInitiationStudent"])
def delete_scientific(studentId: str):
    if not scientific_service.get(studentId):
        raise HTTPException(status_code=404, detail='Scientific Initiation Student not found')
    scientific_service.delete(studentId)
    return {'ok': True}

# CRUD for PostGraduateStudent
@app.post('/postgraduates/', response_model=PostGraduateStudent, summary="Criar postgraduate", tags=["PostGraduateStudent"])
def create_postgraduate(student: PostGraduateStudent):
    """Exemplo de body:
    {
      "name": "Ana Paula",
      "age": 27,
      "studentId": "PG101",
      "thesisTitle": "Deep Learning em Saúde",
      "supervisor": "Dr. Silva",
      "workedDays": 200,
      "scholarshipAmount": 1500.0
    }
    """
    if not student.name or not student.studentId or not student.thesisTitle or not student.supervisor:
        raise HTTPException(status_code=422, detail='Nome, studentId, thesisTitle e supervisor são obrigatórios')
    if student.age < 0 or student.workedDays < 0:
        raise HTTPException(status_code=422, detail='Idade e workedDays não podem ser negativos')
    if student.scholarshipAmount < 0:
        raise HTTPException(status_code=422, detail='scholarshipAmount não pode ser negativo')
    if postgrad_service.get(student.studentId):
        raise HTTPException(status_code=400, detail='PostGraduate Student already exists')
    postgrad_service.add(student)
    return student

@app.post('/postgraduates/batch', response_model=List[PostGraduateStudent], summary="Criar postgraduates em lote", tags=["PostGraduateStudent"])
def create_postgraduates_batch(students: List[PostGraduateStudent] = Body(...)):
    """Cria vários postgraduates de uma vez. Exemplo de body:
    [
      {"name": "Ana Paula", "age": 27, "studentId": "PG101", "thesisTitle": "Deep Learning em Saúde", "supervisor": "Dr. Silva", "workedDays": 200, "scholarshipAmount": 1500.0},
      {"name": "Lucas Costa", "age": 28, "studentId": "PG102", "thesisTitle": "IA em Robótica", "supervisor": "Dra. Souza", "workedDays": 180, "scholarshipAmount": 1400.0}
    ]
    """
    created = []
    ids = set()
    for student in students:
        if not student.name or not student.studentId or not student.thesisTitle or not student.supervisor:
            raise HTTPException(status_code=422, detail='Nome, studentId, thesisTitle e supervisor são obrigatórios para todos os postgraduates')
        if student.age < 0 or student.workedDays < 0:
            raise HTTPException(status_code=422, detail='Idade e workedDays não podem ser negativos para todos os postgraduates')
        if student.scholarshipAmount < 0:
            raise HTTPException(status_code=422, detail='scholarshipAmount não pode ser negativo para todos os postgraduates')
        if student.studentId in ids:
            raise HTTPException(status_code=400, detail=f'Duplicidade de studentId no batch: {student.studentId}')
        if postgrad_service.get(student.studentId):
            raise HTTPException(status_code=400, detail=f'PostGraduate já existe: {student.studentId}')
        ids.add(student.studentId)
        postgrad_service.add(student)
        created.append(student)
    return created

@app.get('/postgraduates/', response_model=List[PostGraduateStudent], summary="Listar postgraduates", tags=["PostGraduateStudent"])
def list_postgraduates():
    return postgrad_service.read_all()

@app.get('/postgraduates/{studentId}', response_model=PostGraduateStudent, summary="Buscar postgraduate", tags=["PostGraduateStudent"])
def get_postgraduate(studentId: str):
    student = postgrad_service.get(studentId)
    if not student:
        raise HTTPException(status_code=404, detail='PostGraduate Student not found')
    return student

@app.put('/postgraduates/{studentId}', response_model=PostGraduateStudent, summary="Atualizar postgraduate", tags=["PostGraduateStudent"])
def update_postgraduate(studentId: str, student: PostGraduateStudent):
    if not postgrad_service.get(studentId):
        raise HTTPException(status_code=404, detail='PostGraduate Student not found')
    postgrad_service.update(studentId, student)
    return student

@app.delete('/postgraduates/{studentId}', summary="Remover postgraduate", tags=["PostGraduateStudent"])
def delete_postgraduate(studentId: str):
    if not postgrad_service.get(studentId):
        raise HTTPException(status_code=404, detail='PostGraduate Student not found')
    postgrad_service.delete(studentId)
    return {'ok': True}
