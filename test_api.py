import requests

BASE_URL = "https://student-management-k1vk.onrender.com"

# Exemplo: criar um estudante
student = {
    "name": "Teste API",
    "age": 25,
    "studentId": "T001"
}
resp = requests.post(f"{BASE_URL}/students/", json=student)
print("POST /students/", resp.status_code, resp.json())

# Exemplo: listar estudantes
resp = requests.get(f"{BASE_URL}/students/")
print("GET /students/", resp.status_code, resp.json())

# Exemplo: buscar estudante por ID
student_id = student["studentId"]
resp = requests.get(f"{BASE_URL}/students/{student_id}")
print(f"GET /students/{{student_id}}", resp.status_code, resp.json())

# Exemplo: atualizar estudante
update = {"name": "Teste Atualizado", "age": 26, "studentId": student_id}
resp = requests.put(f"{BASE_URL}/students/{student_id}", json=update)
print(f"PUT /students/{{student_id}}", resp.status_code, resp.json())

# Exemplo: deletar estudante
resp = requests.delete(f"{BASE_URL}/students/{student_id}")
print(f"DELETE /students/{{student_id}}", resp.status_code, resp.json())
