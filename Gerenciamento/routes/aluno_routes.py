from flask import Blueprint, jsonify, request
from app.controllers.aluno_controller import *
aluno_bp = Blueprint('aluno_bp', __name__)
@aluno_bp.route('/', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return jsonify([{'id': a.id, 'nome': a.nome, 'idade': a.idade, 'turma_id': a.turma_id} for a in alunos])
@aluno_bp.route('/', methods=['POST'])
def add_aluno():
    data = request.get_json()
    novo = criar_aluno(data)
    return jsonify({'id': novo.id, 'nome': novo.nome, 'idade': novo.idade, 'turma_id': novo.turma_id}), 201
@aluno_bp.route('/<int:id>', methods=['GET'])
def get_aluno(id):
    a = obter_aluno(id)
    if not a:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    return jsonify({'id': a.id, 'nome': a.nome, 'idade': a.idade, 'turma_id': a.turma_id})
@aluno_bp.route('/<int:id>', methods=['PUT'])
def update_aluno(id):
    data = request.get_json()
    a = atualizar_aluno(id, data)
    if not a:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    return jsonify({'id': a.id, 'nome': a.nome, 'idade': a.idade, 'turma_id': a.turma_id})
@aluno_bp.route('/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    a = deletar_aluno(id)
    if not a:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    return jsonify({'message': 'Aluno deletado com sucesso'})
