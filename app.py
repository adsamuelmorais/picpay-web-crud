"""Cria uma API Flask para gerenciar usuários.

Esta API permite a criação, leitura, atualização e exclusão de usuários em um
banco de dados SQLite local.

Atributos:
    app (Flask): A instância do Flask que representa a API.
    db (SQLAlchemy): A instância do SQLAlchemy que representa o banco de dados.

Métodos:
    users (GET, POST):
        - GET: Retorna uma lista de todos os usuários no banco de dados.
        - POST: Cria um novo usuário.

    user (GET, PUT, DELETE):
        - GET: Recupera um usuário específico por ID.
        - PUT: Atualiza um usuário existente.
        - DELETE: Exclui um usuário.
"""

import re
from datetime import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)


class User(db.Model):
    """Representa um usuário do sistema."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    birth_date = db.Column(db.Date, unique=False, nullable=False)
    fields_regex = {
     "email": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
     "birth_date": r"^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$",
    }

    def validate_fields(self, payload):
        """Valida os campos de um usuário.

        Verifica se os campos da requisição estão de acordo com as
        expressões regulares definidas em 'fields_regex'.

        Args:
            payload (dict): Dicionário contendo os dados do usuário.

        Raises:
            BadRequest: Se algum campo estiver inválido.
        """
        for field, value in payload.items():
            if field in self.fields_regex and not re.match(
                self.fields_regex[field], value
            ):
                raise BadRequest(
                    f"O valor '{value}' para o campo '{field}' é inválido."
                )


# Cria as tabelas no banco de dados
app.app_context().push()
db.create_all()


# Endpoints
@app.route("/users", methods=["GET", "POST"])
def users():
    """
    - GET: Recupera todos os usuários.
    - POST: Cria um novo usuário.
    """
    if request.method == "POST":
        req_data = request.get_json()
        new_user = User(
            name=req_data["name"],
            email=req_data["email"],
            birth_date=(
                datetime.strptime(req_data["birth_date"], "%Y-%m-%d")
                .date()
                )
        )
        new_user.validate_fields(req_data)
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify({
                "message": "Usuário criado com sucesso",
                "user_id": new_user.id
                }),
            201,
        )
    else:
        users = User.query.all()
        return jsonify([user.json() for user in users])


@app.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"])
def user(id):
    """
    - GET: Recupera um usuário específico.
    - PUT: Atualiza um usuário existente.
    - DELETE: Exclui um usuário.
    """
    try:
        user = User.query.get_or_404(id)
    except NotFound:
        raise NotFound("Usuário não encontrado")

    if request.method == "GET":
        return jsonify(user.json())
    elif request.method == "PUT":
        req_data = request.get_json()
        user.validate_fields(req_data)
        # Recupera os dados pré-existentes na base para evitarmos
        # de solicitar todos os campos
        current_data = user.json()
        updated_data = {**current_data, **req_data}
        user.name = updated_data.get("name")
        user.email = updated_data.get("email")
        user.birth_date = datetime.strptime(
            str(updated_data.get("birth_date")), "%Y-%m-%d"
        ).date()
        db.session.commit()
        return jsonify(
            {"message": "Usuário atualizado com sucesso", "user_id": user.id}
        )
    elif request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            "message": "Usuário deletado com sucesso",
            "user_id": user.id
            })


# Método para serializar os objetos User para JSON
User.json = lambda self: {
    "id": self.id,
    "name": self.name,
    "email": self.email,
    "birth_date": self.birth_date,
}

if __name__ == "__main__":
    app.run(debug=True)
