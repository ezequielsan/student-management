import csv
from typing import List, Type, Any
from app.model.student import Student
from app.model.undergraduate_student import UndergraduateStudent
from app.model.scientific_initiation_student import ScientificInitiationStudent
from app.model.post_graduate_student import PostGraduateStudent

class CSVService:
    def __init__(self, filename: str, schema: Type[Any], fieldnames: List[str]):
        self.filename = filename
        self.schema = schema
        self.fieldnames = fieldnames
        try:
            with open(self.filename, 'x', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
        except FileExistsError:
            pass

    def read_all(self) -> List[Any]:
        with open(self.filename, newline='') as f:
            reader = csv.DictReader(f)
            items = []
            for row in reader:
                # Conversão de tipos conforme necessário
                if 'age' in row and row['age'] != '':
                    row['age'] = int(row['age'])
                if 'workedDays' in row and row['workedDays'] != '':
                    row['workedDays'] = int(row['workedDays'])
                if 'scholarshipAmount' in row and row['scholarshipAmount'] != '':
                    row['scholarshipAmount'] = float(row['scholarshipAmount'])
                items.append(self.schema(**row))
            return items

    def write_all(self, items: List[Any]):
        with open(self.filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item.dict())

    def add(self, item: Any):
        items = self.read_all()
        items.append(item)
        self.write_all(items)

    def update(self, studentId: str, new_item: Any):
        items = self.read_all()
        for i, item in enumerate(items):
            if getattr(item, 'studentId', None) == studentId:
                items[i] = new_item
                break
        self.write_all(items)

    def delete(self, studentId: str):
        items = self.read_all()
        items = [item for item in items if getattr(item, 'studentId', None) != studentId]
        self.write_all(items)

    def get(self, studentId: str) -> Any:
        items = self.read_all()
        for item in items:
            if getattr(item, 'studentId', None) == studentId:
                return item
        return None
