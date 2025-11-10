from app.models.aluno import Aluno
from app import db
def listar_alunos():
    return Aluno.query.all()
def criar_aluno(data):
    novo = Aluno(nome=data['nome'], idade=data['idade'], turma_id=data.get('turma_id'))
    db.session.add(novo)
    db.session.commit()
    return novo
def obter_aluno(id):
    return Aluno.query.get(id)
def atualizar_aluno(id, data):
    a = Aluno.query.get(id)
    if a:
        a.nome = data.get('nome', a.nome)
        a.idade = data.get('idade', a.idade)
        a.turma_id = data.get('turma_id', a.turma_id)
        db.session.commit()
    return a
def deletar_aluno(id):
    a = Aluno.query.get(id)
    if a:
        db.session.delete(a)
        db.session.commit()
    return a
