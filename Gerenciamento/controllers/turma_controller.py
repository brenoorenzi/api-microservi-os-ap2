from app.models.turma import Turma
from app import db
def listar_turmas():
    return Turma.query.all()
def criar_turma(data):
    novo = Turma(nome=data['nome'], professor_id=data.get('professor_id'))
    db.session.add(novo)
    db.session.commit()
    return novo
def obter_turma(id):
    return Turma.query.get(id)
def atualizar_turma(id, data):
    t = Turma.query.get(id)
    if t:
        t.nome = data.get('nome', t.nome)
        t.professor_id = data.get('professor_id', t.professor_id)
        db.session.commit()
    return t
def deletar_turma(id):
    t = Turma.query.get(id)
    if t:
        db.session.delete(t)
        db.session.commit()
    return t
