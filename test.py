import pytest
import requests
import time

# Endereços dos serviços (conforme README)
GEREN_BASE = "http://localhost:8081/api"
RESERV_BASE = "http://localhost:8082/api"
ATIV_BASE = "http://localhost:8083/api"

# Tempo de espera entre tentativas para dar tempo aos serviços subirem (se necessário)
RETRY_DELAY = 0.5
RETRIES = 6

def wait_for(url):
    for _ in range(RETRIES):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(RETRY_DELAY)
    return False

@pytest.fixture(scope="module")
def ctx():
    # Verifica se serviços estão online
    assert wait_for(GEREN_BASE + "/professores"), "Serviço de Gerenciamento indisponível"
    assert wait_for(RESERV_BASE + "/reservas"), "Serviço de Reservas indisponível"
    assert wait_for(ATIV_BASE + "/atividades"), "Serviço de Atividades indisponível"

    created = {}

    # 1) Criar professor (Gerenciamento)
    prof_payload = {"nome": "Test Prof", "idade": 40, "materia": "Testes"}
    r = requests.post(GEREN_BASE + "/professores", json=prof_payload)
    assert r.status_code in (200,201)
    created['professor'] = r.json()
    prof_id = created['professor'].get("id")

    # 2) Criar turma (Gerenciamento) referenciando professor
    turma_payload = {"descricao": "Turma Teste", "professor_id": prof_id}
    r = requests.post(GEREN_BASE + "/turmas", json=turma_payload)
    assert r.status_code in (200,201)
    created['turma'] = r.json()
    turma_id = created['turma'].get("id")

    # 3) Criar aluno (Gerenciamento) referenciando turma
    aluno_payload = {
        "nome": "Aluno Teste",
        "idade": 20,
        "data_nascimento": "01/01/2005",
        "nota_1_semestre": 7.0,
        "nota_2_semestre": 8.0,
        "turma_id": turma_id
    }
    r = requests.post(GEREN_BASE + "/alunos", json=aluno_payload)
    assert r.status_code in (200,201)
    created['aluno'] = r.json()
    created_ids = {
        "professor_id": prof_id,
        "turma_id": turma_id,
        "aluno_id": created['aluno'].get("id")
    }

    yield created_ids

    # Teardown: tenta apagar na ordem dependente (Notas/Atividades/Reservas -> Gerenciamento)
    # 1) Deletar notas e atividades (no serviço de Atividades)
    try:
        # Deleta todas as notas e atividades criadas por teste (procura por aluno/atividade relacionados pelo nome)
        r = requests.get(ATIV_BASE + "/notas")
        if r.ok:
            for n in r.json():
                if n.get("aluno_id") == created_ids["aluno_id"]:
                    requests.delete(ATIV_BASE + f"/notas/{n.get('id')}")
    except Exception:
        pass

    try:
        r = requests.get(ATIV_BASE + "/atividades")
        if r.ok:
            for a in r.json():
                if a.get("professor_id") == created_ids["professor_id"] or a.get("turma_id") == created_ids["turma_id"]:
                    requests.delete(ATIV_BASE + f"/atividades/{a.get('id')}")
    except Exception:
        pass

    # 2) Deletar reservas
    try:
        r = requests.get(RESERV_BASE + "/reservas")
        if r.ok:
            for rv in r.json():
                if rv.get("turma_id") == created_ids["turma_id"]:
                    requests.delete(RESERV_BASE + f"/reservas/{rv.get('id')}")
    except Exception:
        pass

    # 3) Deletar aluno, turma, professor no gerenciamento
    try:
        requests.delete(GEREN_BASE + f"/alunos/{created_ids['aluno_id']}")
    except Exception:
        pass
    try:
        requests.delete(GEREN_BASE + f"/turmas/{created_ids['turma_id']}")
    except Exception:
        pass
    try:
        requests.delete(GEREN_BASE + f"/professores/{created_ids['professor_id']}")
    except Exception:
        pass

def test_reservas_crud(ctx):
    turma_id = ctx["turma_id"]

    # CREATE reserva
    payload = {"num_sala": 101, "lab": False, "data_reserva": "25/10/2025", "turma_id": turma_id}
    r = requests.post(RESERV_BASE + "/reservas", json=payload)
    assert r.status_code in (200,201)
    reserva = r.json()
    rid = reserva.get("id")

    # READ list
    r = requests.get(RESERV_BASE + "/reservas")
    assert r.status_code == 200
    assert any(rv.get("id") == rid for rv in r.json())

    # READ single
    r = requests.get(RESERV_BASE + f"/reservas/{rid}")
    assert r.status_code == 200
    assert r.json().get("id") == rid

    # UPDATE
    upd = {"num_sala": 202, "lab": True}
    r = requests.put(RESERV_BASE + f"/reservas/{rid}", json=upd)
    assert r.status_code == 200
    assert r.json().get("num_sala") == 202

    # DELETE
    r = requests.delete(RESERV_BASE + f"/reservas/{rid}")
    assert r.status_code in (200,204)

def test_atividades_e_notas_crud(ctx):
    turma_id = ctx["turma_id"]
    prof_id = ctx["professor_id"]
    aluno_id = ctx["aluno_id"]

    # CREATE atividade
    payload = {
        "nome_atividade": "Atividade Teste",
        "descricao": "Descrição",
        "peso_porcento": 20,
        "data_entrega": "30/11/2025",
        "turma_id": turma_id,
        "professor_id": prof_id
    }
    r = requests.post(ATIV_BASE + "/atividades", json=payload)
    assert r.status_code in (200,201)
    atividade = r.json()
    aid = atividade.get("id")

    # READ atividades
    r = requests.get(ATIV_BASE + "/atividades")
    assert r.status_code == 200
    assert any(a.get("id") == aid for a in r.json())

    # UPDATE atividade
    r = requests.put(ATIV_BASE + f"/atividades/{aid}", json={"descricao": "Atualizada"})
    assert r.status_code == 200
    assert r.json().get("descricao") == "Atualizada"

    # CREATE nota (usa aluno do Gerenciamento e atividade criada)
    nota_payload = {"nota_atividade": 9.5, "aluno_id": aluno_id, "atividade_id": aid}
    r = requests.post(ATIV_BASE + "/notas", json=nota_payload)
    assert r.status_code in (200,201)
    nota = r.json()
    nid = nota.get("id")

    # READ notas
    r = requests.get(ATIV_BASE + "/notas")
    assert r.status_code == 200
    assert any(n.get("id") == nid for n in r.json())

    # UPDATE nota
    r = requests.put(ATIV_BASE + f"/notas/{nid}", json={"nota_atividade": 8.0})
    assert r.status_code == 200
    assert float(r.json().get("nota_atividade")) == 8.0

    # DELETE nota and atividade
    r = requests.delete(ATIV_BASE + f"/notas/{nid}")
    assert r.status_code in (200,204)
    r = requests.delete(ATIV_BASE + f"/atividades/{aid}")
    assert r.status_code in (200,204)

def test_gerenciamento_crud_direct():
    # Professores CRUD
    prof = {"nome": "Prof CRUD", "idade": 50, "materia": "CRUD"}
    r = requests.post(GEREN_BASE + "/professores", json=prof)
    assert r.status_code in (200,201)
    pid = r.json().get("id")

    r = requests.get(GEREN_BASE + f"/professores/{pid}")
    assert r.status_code == 200

    r = requests.put(GEREN_BASE + f"/professores/{pid}", json={"idade": 51})
    assert r.status_code == 200
    assert r.json().get("idade") == 51

    # Turmas CRUD
    turma = {"descricao": "Turma CRUD", "professor_id": pid}
    r = requests.post(GEREN_BASE + "/turmas", json=turma)
    assert r.status_code in (200,201)
    tid = r.json().get("id")

    r = requests.get(GEREN_BASE + f"/turmas/{tid}")
    assert r.status_code == 200

    r = requests.put(GEREN_BASE + f"/turmas/{tid}", json={"descricao": "Atualizada CRUD"})
    assert r.status_code == 200

    # Alunos CRUD
    aluno = {
        "nome": "Aluno CRUD",
        "idade": 18,
        "data_nascimento": "02/02/2007",
        "nota_1_semestre": 6.0,
        "nota_2_semestre": 7.0,
        "turma_id": tid
    }
    r = requests.post(GEREN_BASE + "/alunos", json=aluno)
    assert r.status_code in (200,201)
    aid = r.json().get("id")

    r = requests.get(GEREN_BASE + f"/alunos/{aid}")
    assert r.status_code == 200

    r = requests.put(GEREN_BASE + f"/alunos/{aid}", json={"nome": "Aluno CRUD Atualizado"})
    assert r.status_code == 200
    assert "Aluno CRUD Atualizado" in r.json().get("nome")

    # Cleanup
    requests.delete(GEREN_BASE + f"/alunos/{aid}")
    requests.delete(GEREN_BASE + f"/turmas/{tid}")
    requests.delete(GEREN_BASE + f"/professores/{pid}")