from app.models.professor import Professor
from app import db
def listar_professores():
    return Professor.query.all()
def criar_professor(data):
    novo = Professor(nome=data['nome'], disciplina=data['disciplina'])
    db.session.add(novo)
    db.session.commit()
    return novo
def obter_professor(id):
    return Professor.query.get(id)
def atualizar_professor(id, data):
    prof = Professor.query.get(id)
    if prof:
        prof.nome = data.get('nome', prof.nome)
        prof.disciplina = data.get('disciplina', prof.disciplina)
        db.session.commit()
    return prof
def deletar_professor(id):
    prof = Professor.query.get(id)
    if prof:
        db.session.delete(prof)
        db.session.commit()
    return prof
