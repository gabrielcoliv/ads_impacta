# config.py
import os

DB_HOST = "localhost"
DB_NAME = "meu_sistema"  # Nome do seu banco de dados
DB_USER = "postgres"  # Seu usuário no PostgreSQL
DB_PASSWORD = "123"  # Sua senha do PostgreSQL

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
