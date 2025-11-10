from flask import Blueprint, jsonify, request
from app.controllers.turma_controller import *
turma_bp = Blueprint('turma_bp', __name__)
@turma_bp.route('/', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return jsonify([{'id': t.id, 'nome': t.nome, 'professor_id': t.professor_id} for t in turmas])
@turma_bp.route('/', methods=['POST'])
def add_turma():
    data = request.get_json()
    novo = criar_turma(data)
    return jsonify({'id': novo.id, 'nome': novo.nome, 'professor_id': novo.professor_id}), 201
@turma_bp.route('/<int:id>', methods=['GET'])
def get_turma(id):
    t = obter_turma(id)
    if not t:
        return jsonify({'error': 'Turma não encontrada'}), 404
    return jsonify({'id': t.id, 'nome': t.nome, 'professor_id': t.professor_id})
@turma_bp.route('/<int:id>', methods=['PUT'])
def update_turma(id):
    data = request.get_json()
    t = atualizar_turma(id, data)
    if not t:
        return jsonify({'error': 'Turma não encontrada'}), 404
    return jsonify({'id': t.id, 'nome': t.nome, 'professor_id': t.professor_id})
@turma_bp.route('/<int:id>', methods=['DELETE'])
def delete_turma(id):
    t = deletar_turma(id)
    if not t:
        return jsonify({'error': 'Turma não encontrada'}), 404
    return jsonify({'message': 'Turma deletada com sucesso'})
