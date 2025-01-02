import re
from datetime import datetime

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

from models import User, db

crud_bp = Blueprint('crud_bp', __name__)


def validate_fields(payload: dict) -> None:
    """Valida os campos de um usuário.

    Verifica se os campos da requisição estão de acordo com as
    expressões regulares definidas em 'fields_regex'.

    Args:
        payload (dict): Dicionário contendo os dados do usuário.

    Raises:
        BadRequest: Se algum campo estiver inválido.
    """
    for field, value in payload.items():
        if field in User.fields_regex and not re.match(
            User.fields_regex[field], value
        ):
            raise BadRequest(
                f"O valor '{value}' para o campo '{field}' é inválido."
            )


# Endpoints
@crud_bp.route("/users", methods=["GET", "POST"])
def users():
    """
    - GET: Recupera todos os usuários.
    - POST: Cria um novo usuário.
    """
    if request.method == "POST":
        req_data = request.get_json()
        validate_fields(req_data)
        new_user = User(
            name=req_data["name"],
            email=req_data["email"],
            birth_date=(
                datetime.strptime(req_data["birth_date"], "%Y-%m-%d")
                .date()
                )
        )
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


@crud_bp.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"])
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
        validate_fields(req_data)
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
