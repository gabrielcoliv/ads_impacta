from flask_sqlalchemy import SQLAlchemy

# Criar o objeto db
db = SQLAlchemy()

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    endereco = db.Column(db.Text)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)
    
    # Defina o relacionamento na classe Fornecedor
    produtos = db.relationship('Produto', backref='fornecedor', lazy='joined')

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, default=0)
    
    # Chave estrangeira para Fornecedor
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)
