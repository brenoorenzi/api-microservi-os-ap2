from flask import Blueprint, jsonify, request
from app.controllers.professor_controller import *
professor_bp = Blueprint('professor_bp', __name__)
@professor_bp.route('/', methods=['GET'])
def get_professores():
    professores = listar_professores()
    return jsonify([{'id': p.id, 'nome': p.nome, 'disciplina': p.disciplina} for p in professores])
@professor_bp.route('/', methods=['POST'])
def add_professor():
    data = request.get_json()
    novo = criar_professor(data)
    return jsonify({'id': novo.id, 'nome': novo.nome, 'disciplina': novo.disciplina}), 201
@professor_bp.route('/<int:id>', methods=['GET'])
def get_professor(id):
    p = obter_professor(id)
    if not p:
        return jsonify({'error': 'Professor não encontrado'}), 404
    return jsonify({'id': p.id, 'nome': p.nome, 'disciplina': p.disciplina})
@professor_bp.route('/<int:id>', methods=['PUT'])
def update_professor(id):
    data = request.get_json()
    p = atualizar_professor(id, data)
    if not p:
        return jsonify({'error': 'Professor não encontrado'}), 404
    return jsonify({'id': p.id, 'nome': p.nome, 'disciplina': p.disciplina})
@professor_bp.route('/<int:id>', methods=['DELETE'])
def delete_professor(id):
    p = deletar_professor(id)
    if not p:
        return jsonify({'error': 'Professor não encontrado'}), 404
    return jsonify({'message': 'Professor deletado com sucesso'})
