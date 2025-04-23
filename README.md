# 🩺 Projeto Prontuário Digital

Este projeto tem como objetivo automatizar a leitura, extração, armazenamento e manipulação de dados de pacientes a partir de arquivos PDF preenchíveis. A aplicação fornece uma API RESTful que permite operações de CRUD sobre os registros extraídos.

## 🚀 Funcionalidades

- 📄 Leitura de arquivos PDF preenchíveis com dados de pacientes
- 🧠 Extração dos seguintes campos:
  - Nome completo
  - Data de nascimento
  - Endereço
  - Profissão
  - Telefone
  - Email
  - Nome do pai
  - Idade do pai
  - Nome da mãe
  - Idade da mãe
  - Queixa principal
- 🗃️ Armazenamento dos dados em banco de dados relacional
- 📡 API RESTful com as seguintes rotas:
  - `GET /users` → Retorna todos os registros
  - `GET /users/{id}` → Retorna os dados de um paciente específico
  - `PATCH /users/{id}` → Atualiza dados de um paciente
  - `DELETE /users/{id}` → Remove um paciente do banco
- 🔄 Preenchimento e exportação de novos PDFs com dados da base
- 🧪 Testes realizados via Postman
- 🧱 Estrutura baseada em camadas:
  - `controller/`
  - `service/`
  - `repositories/`

## 🛠 Tecnologias Utilizadas

- Python 3.12
- FastAPI
- Uvicorn
- SQLite / PostgreSQL (configurável)
- Pydantic
- pdfplumber
- Postman (para testes manuais)
