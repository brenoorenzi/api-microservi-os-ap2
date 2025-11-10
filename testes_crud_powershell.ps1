# Testes CRUD dos microserviços via terminal (PowerShell)
# Execute cada comando no PowerShell, alterando IDs conforme necessário

# ----------- CRUD Reservas (porta 5002) -----------
# Criar reserva
Invoke-RestMethod -Uri http://localhost:5002/reservas/ -Method POST -ContentType 'application/json' -Body '{"num_sala": 101, "lab": true, "data": "2025-12-01", "turma_id": 1}'

# Listar reservas
Invoke-RestMethod -Uri http://localhost:5002/reservas/ -Method GET

# Buscar reserva por ID (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5002/reservas/1 -Method GET

# Atualizar reserva (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5002/reservas/1 -Method PUT -ContentType 'application/json' -Body '{"num_sala": 102, "lab": false, "data": "2025-12-02", "turma_id": 2}'

# Deletar reserva (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5002/reservas/1 -Method DELETE


# ----------- CRUD Notas (porta 5001) -----------
# Criar nota
Invoke-RestMethod -Uri http://localhost:5001/notas/ -Method POST -ContentType 'application/json' -Body '{"nota": 8.5, "aluno_id": 1, "atividade_id": 1}'

# Listar notas
Invoke-RestMethod -Uri http://localhost:5001/notas/ -Method GET

# Buscar nota por ID (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5001/notas/1 -Method GET

# Atualizar nota (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5001/notas/1 -Method PUT -ContentType 'application/json' -Body '{"nota": 9.0, "aluno_id": 1, "atividade_id": 1}'

# Deletar nota (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5001/notas/1 -Method DELETE


# ----------- CRUD Atividades (porta 5001) -----------
# Criar atividade
Invoke-RestMethod -Uri http://localhost:5001/atividades/ -Method POST -ContentType 'application/json' -Body '{"nome_atividade": "Aula Teste", "descricao": "Descrição de teste", "peso_porcento": 10, "data_entrega": "2025-12-01", "professor_id": 1, "turma_id": 1}'

# Listar atividades
Invoke-RestMethod -Uri http://localhost:5001/atividades/ -Method GET

# Buscar atividade por ID (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5001/atividades/1 -Method GET

# Atualizar atividade (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5001/atividades/1 -Method PUT -ContentType 'application/json' -Body '{"nome_atividade": "Aula Atualizada", "descricao": "Nova descrição", "peso_porcento": 20, "data_entrega": "2025-12-02", "professor_id": 1, "turma_id": 1}'

# Deletar atividade (exemplo: 1)
Invoke-RestMethod -Uri http://localhost:5001/atividades/1 -Method DELETE
