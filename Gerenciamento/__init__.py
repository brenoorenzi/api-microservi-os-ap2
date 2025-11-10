from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from app.config import Config

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    Swagger(app, template_file='app/swagger/swagger.yaml')
    from app.routes.professor_routes import professor_bp
    from app.routes.aluno_routes import aluno_bp
    from app.routes.turma_routes import turma_bp
    app.register_blueprint(professor_bp, url_prefix='/api/professores')
    app.register_blueprint(aluno_bp, url_prefix='/api/alunos')
    app.register_blueprint(turma_bp, url_prefix='/api/turmas')
    with app.app_context():
        db.create_all()
    return app
