from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


# Método para serializar os objetos User para JSON
User.json = lambda self: {
    "id": self.id,
    "name": self.name,
    "email": self.email,
    "birth_date": self.birth_date,
}
