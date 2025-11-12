# Ecossistema de Microsserviços de Gestão Escolar

Este projeto implementa uma solução **distribuída** para a gestão de uma instituição de ensino, utilizando uma arquitetura de **microsserviços** para separar as responsabilidades em domínios de negócio autônomos.

O ecossistema é composto por três APIs Flask independentes, cada uma com sua própria persistência de dados (SQLite), orquestradas e containerizadas via **Docker Compose**.

---

## Componentes do Ecossistema

O sistema é dividido em três serviços principais, cada um focado em uma área de responsabilidade específica:

| Serviço | Domínio de Negócio | Responsabilidades Principais | Porta Padrão |
| :--- | :--- | :--- | :--- |
| **Gerenciamento** | Fonte da Verdade (Core) | Gerencia **Professores**, **Turmas** e **Alunos**. | `8081` |
| **Reservas** | Agendamento | Gerencia o agendamento e **reservas de salas**. | `8082` |
| **Atividades** | Avaliação | Controla **atividades** pedagógicas e o lançamento de **notas**. | `8083` |

---

## Desenvolvedores

| Nome | RA |
| :--- | :--- |
| **Gustavo Silva Matos** | 2400891 |
| **Caliu Muriell** | 2404012 |
| **Nicole Moraes Ferreira** | 2403651 |
| **Breno Gonçalves Renzi Del Cacho** | 2403703 |

---

## Stack Tecnológico

| Categoria | Ferramentas |
| :--- | :--- |
| **Linguagem / Framework** | Python, Flask |
| **Persistência** | SQLite, Flask-SQLAlchemy (ORM) |
| **Comunicação** | Flask-Cors, Requests (para chamadas inter-serviços) |
| **Documentação** | Flasgger (Gera Swagger UI) |
| **Infraestrutura** | Docker, Docker Compose |

---

## Guia de Execução (via Docker)

O **Docker Compose** é o método recomendado para iniciar o projeto, pois ele constrói, configura e conecta todos os três microsserviços em uma rede virtual unificada.

### Pré-requisito

* Ter o **Docker Desktop** instalado e em execução.

### Passo 1: Construção das Imagens

No diretório raiz do projeto (onde o `docker-compose.yml` reside), execute:

```bash
docker-compose build
