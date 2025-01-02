"""
Cria e configura uma instância do aplicativo Flask.

Inicializa um aplicativo Flask, configura a conexão com o banco de dados,
registra o blueprint para operações CRUD e cria as tabelas do banco
de dados (se elas não existirem).

Retorna:
    Uma instância configurada do aplicativo Flask.
"""

from flask import Flask

from routes import crud_bp
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db.init_app(app)

app.register_blueprint(crud_bp)

# Cria as tabelas no banco de dados
app.app_context().push()
db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
