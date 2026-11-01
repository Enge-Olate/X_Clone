# X Clone

Clone da rede social X desenvolvido com Django,
Django REST Framework e PostgreSQL.

## Funcionalidades

- Cadastro de usuários
- Login
- Recuperação de senha
- Perfis de usuário
- Seguir usuários
- Timeline personalizada
- Curtidas
- Reposts
- Respostas
- Notificações

## Tecnologias

- Python
- Django
- DRF
- PostgreSQL
- HTMX
- Tailwind CSS
- Poetry

## Instalação

git clone ...

poetry install

cp .env.example .env

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

## Testes

pytest

## Cobertura

pytest --cov

## Deploy

Consultar docs/deploy.md