from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from models import db, Empresa, Fornecedor, Produto, Cliente
from sqlalchemy.orm import joinedload

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Rota principal com links para os cadastros
@app.route('/')
def index():
    return render_template('index.html')

# Rota para Cadastro de Empresa
@app.route('/empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    if request.method == 'POST':
        # Processar o envio do formulário, como você já fez
        dados = request.get_json()  # Recebe os dados no formato JSON
        nome = dados.get('nome')
        cnpj = dados.get('cnpj')
        endereco = dados.get('endereco', '')
        telefone = dados.get('telefone', '')
        email = dados.get('email', '')
        
        nova_empresa = Empresa(
            nome=nome,
            cnpj=cnpj,
            endereco=endereco,
            telefone=telefone,
            email=email
        )
        db.session.add(nova_empresa)
        db.session.commit()
        return jsonify({"mensagem": "Empresa cadastrada com sucesso!"}), 201
    
    # Aqui você adiciona o método GET para renderizar o formulário
    return render_template('empresa.html')

# Rota para consultar as empresas cadastradas
@app.route('/empresas', methods=['GET'])
def listar_empresas():
    empresas = Empresa.query.all()
    return render_template('consultar_empresas.html', empresas=empresas)

# Rota para Cadastro de Fornecedor
@app.route('/fornecedor', methods=['GET', 'POST'])
def cadastro_fornecedor():
    if request.method == 'POST':
        try:
            nome = request.json.get('nome')
            cnpj = request.json.get('cnpj')
            telefone = request.json.get('telefone', '')
            email = request.json.get('email', '')

            # Verificar o que está sendo recebido
            print(f"Nome: {nome}, CNPJ: {cnpj}, Telefone: {telefone}, Email: {email}")
            
            novo_fornecedor = Fornecedor(
                nome=nome,
                cnpj=cnpj,
                telefone=telefone,
                email=email
            )
            db.session.add(novo_fornecedor)
            db.session.commit()
            return jsonify({"mensagem": "Fornecedor cadastrado com sucesso!"}), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400
    return render_template('fornecedor.html')

# Rota para consultar os fornecedores cadastrados
@app.route('/fornecedores', methods=['GET'])
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()  # Consultando todos os fornecedores
    return render_template('consultar_fornecedores.html', fornecedores=fornecedores)

# Rota para Cadastro de Produto
@app.route('/produto', methods=['GET', 'POST'])
def cadastro_produto():
    if request.method == 'POST':
        try:
            # Captura os dados como JSON
            nome = request.json.get('nome')
            descricao = request.json.get('descricao', '')
            preco = request.json.get('preco')
            estoque = request.json.get('estoque', 0)
            fornecedor_id = request.json.get('fornecedor_id')

            # Verificar os dados recebidos
            print(f"Nome: {nome}, Descrição: {descricao}, Preço: {preco}, Estoque: {estoque}, Fornecedor ID: {fornecedor_id}")
            
            # Criar um novo produto
            novo_produto = Produto(
                nome=nome,
                descricao=descricao,
                preco=preco,
                estoque=estoque,
                fornecedor_id=fornecedor_id
            )
            db.session.add(novo_produto)
            db.session.commit()
            return jsonify({"mensagem": "Produto cadastrado com sucesso!"}), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400
    return render_template('produto.html')

# Rota para consultar os produtos cadastrados
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    # Consulta todos os produtos com o relacionamento do fornecedor
    produtos = Produto.query.join(Fornecedor).all()  # Fazendo join entre Produto e Fornecedor

    # Passando os produtos para o template
    return render_template('consultar_produtos.html', produtos=produtos)

# Rota para Cadastro de Cliente
@app.route('/cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        # Recebe os dados em formato JSON
        data = request.get_json()  # Dados enviados no formato JSON
        
        nome = data.get('nome')
        cpf = data.get('cpf')
        telefone = data.get('telefone', '')
        email = data.get('email', '')
        
        # Cria o novo cliente
        novo_cliente = Cliente(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email
        )
        
        # Adiciona e faz commit no banco de dados
        db.session.add(novo_cliente)
        db.session.commit()
        
        return jsonify({"mensagem": "Cliente cadastrado com sucesso!"}), 201  # Retorna a resposta em JSON
    
    return render_template('cliente.html')

# Rota para consultar os clientes cadastrados
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('consultar_clientes.html', clientes=clientes)

# Execução da API
if __name__ == '__main__':
    app.run(debug=True)
