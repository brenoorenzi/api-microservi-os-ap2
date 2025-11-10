from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/turmas/<int:turma_id>')
def get_turma(turma_id):
    return jsonify({
        'id': turma_id,
        'nome': f'Turma {turma_id}',
        'descricao': 'Turma de exemplo',
    })

@app.route('/professores/<int:professor_id>')
def get_professor(professor_id):
    return jsonify({
        'id': professor_id,
        'nome': f'Professor {professor_id}',
        'disciplina': 'Disciplina Exemplo',
    })

@app.route('/alunos/<int:aluno_id>')
def get_aluno(aluno_id):
    return jsonify({
        'id': aluno_id,
        'nome': f'Aluno {aluno_id}',
        'matricula': f'2025{aluno_id:04d}',
    })

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
