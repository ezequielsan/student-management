# Student Management API

API para gerenciamento de estudantes, desenvolvida com FastAPI e persistência em arquivos CSV.

## Funcionalidades

- CRUD completo para as entidades:
  - Student
  - UndergraduateStudent
  - ScientificInitiationStudent
  - PostGraduateStudent
- Endpoints para criação em lote (batch) de cada entidade
- Validação de dados obrigatórios e duplicidade
- Persistência dos dados em arquivos CSV (enquanto a aplicação estiver rodando)
- Documentação automática e exemplos de uso em `/docs`

## Como rodar localmente

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/student-management.git
   cd student-management
   ```
2. **Crie e ative um ambiente virtual:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Execute a aplicação:**
   ```sh
   uvicorn app.main:app --reload
   ```
5. **Acesse a documentação interativa:**
   - [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints principais

- `POST   /students/` — Cria um estudante
- `POST   /students/batch` — Cria vários estudantes de uma vez
- `GET    /students/` — Lista todos os estudantes
- `GET    /students/{studentId}` — Busca estudante por ID
- `PUT    /students/{studentId}` — Atualiza estudante
- `DELETE /students/{studentId}` — Remove estudante

Mesma lógica para as entidades:
- `/undergraduates/`
- `/scientifics/`
- `/postgraduates/`

## Observações sobre persistência
- Os dados são salvos em arquivos CSV na pasta `data/`.
- Em ambientes de nuvem gratuitos (ex: Render), os dados podem ser perdidos após reinício ou deploy.
- Para produção, recomenda-se uso de banco de dados.

## Estrutura de diretórios
```
app/
  main.py                # Entrypoint da API
  services.py            # Serviços de persistência em CSV
  model/                 # Modelos das entidades
    student.py
    undergraduate_student.py
    scientific_initiation_student.py
    post_graduate_student.py
requirements.txt         # Dependências
README.md                # Este arquivo
.gitignore               # Arquivos ignorados no git
data/                    # Arquivos CSV de dados
```

## Exemplo de requisição (Student)
```json
POST /students/
{
  "name": "João Silva",
  "age": 20,
  "studentId": "S123"
}
```

## Licença
MIT
