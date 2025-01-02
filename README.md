# Desenvolvimento de Aplicação CRUD com Flask

## Descrição:
Este projeto é uma aplicação Flask simples que permite realizar operações CRUD (Criar, Ler, Atualizar, Deletar) em uma entidade de "Usuário". Os dados são persistidos em um banco de dados SQLite.

**Tecnologias:**
* Python
* Flask
* SQLAlchemy
* SQLite
* Docker

## Pré-requisitos
* Docker devidamente instalado: [docs](https://docs.docker.com/engine/install/)

## Preparação:
1. Clone o repositório: `git clone https://github.com/seu_usuario/seu_repositorio.git`
2. Dê permissão de execução no arquivo start.sh para que a aplicação possa ser executada (linux)
```bash
chmod +x start.sh
```

## Execução:
```bash
Execute o arquivo start.sh
```

## Requisições:

1. Retorna a lista de todos os usuários.
```bash
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/users
```
2. Retorna os detalhes de um usuário específico.
```bash
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/users/1
```
3. Adiciona um novo usuário.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Mario Silva", "email": "mario@gmail.com", "birth_date": "1987-06-01"}' http://127.0.0.1:5000/users
```
4. Atualiza os dados de um usuário existente.
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"email": "teste@gmail.com"}' http://127.0.0.1:5000/users/1
```
5. Remove um usuário.
```bash
curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:5000/users/1
```

## Testes

Para executar testes unitários
```bash
pytest
```

## Melhorias
* Dedicar um arquivo "requirements.txt" somente para testes
* Criação de chave de autenticação na api
* Criação de base de dados separada (fora) da aplicação
* CI/CD para deploy e testes unitários para implantação no AWS Lambda ou ferramenta análoga
