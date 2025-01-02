import os
import sys

import pytest

# Adicionando o diretório pai para sys.path
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_path, 'src'))
from app import app, db


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        db.session.remove()
        db.drop_all()


def test_create_user(client):
    data = {
        'name': 'João Silva',
        'email': 'joao@email.com',
        'birth_date': '1987-06-01'
        }
    response = client.post('/users', json=data)
    assert response.status_code == 201
    assert response.json['message'] == 'Usuário criado com sucesso'


def test_create_user_invalid_email(client):
    data = {
        'name': 'João Silva',
        'email': 'invalid_email',
        'birth_date': '1987-06-01'
        }
    response = client.post('/users', json=data)
    assert response.status_code == 400


def test_create_user_invalid_birthdate(client):
    data = {
        'name': 'João Silva',
        'email': 'joao@gmail.com',
        'birth_date': '1500-06-01'
        }
    response = client.post('/users', json=data)
    assert response.status_code == 400


def test_get_user_by_id(client):
    # Cria um usuário
    data = {
        'name': 'João Silva',
        'email': 'joao@email.com',
        'birth_date': '1987-06-01'
        }
    response = client.post('/users', json=data)
    assert response.status_code == 201

    user_id = response.json.get("user_id")
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'João Silva'


def test_get_user_not_found(client):
    response = client.get('/users/999')
    assert response.status_code == 404


def test_update_user(client):
    # Cria um usuário
    data = {
        'name': 'João Silva',
        'email': 'joao@email.com',
        'birth_date': '1987-06-01'
        }
    response = client.post('/users', json=data)
    assert response.status_code == 201

    user_id = response.json.get("user_id")
    data = {'name': 'Maria Silva'}
    response = client.put(f'/users/{user_id}', json=data)
    assert response.status_code == 200

    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Maria Silva'


def test_delete_nonexistent_user(client):
    response = client.delete('/users/999')
    assert response.status_code == 404
