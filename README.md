# API Microserviços — AP2

Este projeto implementa uma arquitetura de microserviços em Python, composta por dois módulos principais:

- AtividadesNotas — gerenciamento de atividades e notas.
- Reservas — controle de reservas e recursos relacionados.

Cada serviço é independente e se comunica via HTTP (REST API).

---

## Estrutura do Projeto

api-microservi-os-ap2-main/
│
├── AtividadesNotas/
│ ├── app.py
│ ├── config.py
│ ├── docker-compose.yml
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── controllers/
│ ├── models/
│ └── instance/database.db
│
├── Reservas/
│ ├── app.py
│ ├── config.py
│ ├── docker-compose.yml
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── controllers/
│ └── models/
│
├── docker-compose.yml
├── README.md
└── requirements.txt


---

## Pré-requisitos

Antes de rodar o projeto, é necessário ter instalado:

- Python 3.10 ou superior
- pip
- Docker
- Docker Compose

---

## Executando com Python (modo local)

Cada serviço pode ser executado separadamente, sem necessidade de Docker.

### AtividadesNotas

```bash
cd AtividadesNotas
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
