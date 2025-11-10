import requests

BASE_URL = "http://localhost:5001/notas"

def test_crud_notas():
    # 1. Criar nota
    payload = {"nota": 8.5, "aluno_id": 1, "atividade_id": 1}
    r = requests.post(BASE_URL + "/", json=payload)
    assert r.status_code == 201, f"POST falhou: {r.text}"
    nota = r.json()
    nota_id = nota["id"]
    print("POST OK", nota)

    # 2. Listar notas
    r = requests.get(BASE_URL + "/")
    assert r.status_code == 200, f"GET all falhou: {r.text}"
    notas = r.json()
    assert any(n["id"] == nota_id for n in notas), "Nota criada não encontrada na listagem"
    print("GET all OK")

    # 3. Buscar nota por ID
    r = requests.get(f"{BASE_URL}/{nota_id}")
    assert r.status_code == 200, f"GET by id falhou: {r.text}"
    print("GET by id OK")

    # 4. Atualizar nota
    update = {"nota": 9.0, "aluno_id": 1, "atividade_id": 1}
    r = requests.put(f"{BASE_URL}/{nota_id}", json=update)
    assert r.status_code == 200, f"PUT falhou: {r.text}"
    assert r.json()["nota"] == 9.0, "Nota não foi atualizada"
    print("PUT OK")

    # 5. Deletar nota
    r = requests.delete(f"{BASE_URL}/{nota_id}")
    assert r.status_code == 200, f"DELETE falhou: {r.text}"
    print("DELETE OK")

    # 6. Confirmar deleção
    r = requests.get(f"{BASE_URL}/{nota_id}")
    assert r.status_code == 404, "Nota não foi deletada"
    print("Confirmação de deleção OK")

if __name__ == "__main__":
    test_crud_notas()
    print("Todos os testes de CRUD de Notas passaram!")
