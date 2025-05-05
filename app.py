from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from models import db, Empresa, Fornecedor, Produto, Cliente, NotaFiscalCompra, NotaFiscalItem, NotaFiscalVenda, NotaFiscalVendaItem
from sqlalchemy.orm import joinedload

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    if request.method == 'POST':
        dados = request.get_json()
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

    return render_template('empresa.html')

@app.route('/empresas', methods=['GET'])
def listar_empresas():
    empresas = Empresa.query.all()
    return render_template('consultar_empresas.html', empresas=empresas)

@app.route('/fornecedor', methods=['GET', 'POST'])
def cadastro_fornecedor():
    if request.method == 'POST':
        try:
            nome = request.json.get('nome')
            cnpj = request.json.get('cnpj')
            telefone = request.json.get('telefone', '')
            email = request.json.get('email', '')

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

@app.route('/fornecedores', methods=['GET'])
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('consultar_fornecedores.html', fornecedores=fornecedores)

@app.route('/fornecedores_json', methods=['GET'])
def fornecedores_json():
    fornecedores = Fornecedor.query.with_entities(Fornecedor.id, Fornecedor.nome).all()
    return jsonify([{"id": f.id, "nome": f.nome} for f in fornecedores])

@app.route('/produto', methods=['GET', 'POST'])
def cadastro_produto():
    if request.method == 'POST':
        try:
            nome = request.json.get('nome')
            descricao = request.json.get('descricao', '')
            preco = request.json.get('preco')
            estoque = request.json.get('estoque', 0)
            fornecedor_id = request.json.get('fornecedor_id')

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

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.join(Fornecedor).all()
    return render_template('consultar_produtos.html', produtos=produtos)

@app.route('/produtos_json', methods=['GET'])
def produtos_json():
    produtos = Produto.query.with_entities(Produto.id, Produto.nome).all()
    return jsonify([{"id": p.id, "nome": p.nome} for p in produtos])

@app.route('/cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        data = request.get_json()
        nome = data.get('nome')
        cpf = data.get('cpf')
        telefone = data.get('telefone', '')
        email = data.get('email', '')

        novo_cliente = Cliente(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email
        )
        db.session.add(novo_cliente)
        db.session.commit()
        return jsonify({"mensagem": "Cliente cadastrado com sucesso!"}), 201

    return render_template('cliente.html')

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('consultar_clientes.html', clientes=clientes)

@app.route('/nota_fiscal_compra', methods=['GET', 'POST'])
def nota_fiscal_compra():
    if request.method == 'POST':
        data = request.get_json()

        nota = NotaFiscalCompra(
            numero=data['numero'],
            serie=data['serie'],
            data_emissao=data['data_emissao'],
            fornecedor_id=data['fornecedor_id'],
            valor_total=data['valor_total']
        )
        db.session.add(nota)
        db.session.flush()  # Para obter o ID da nota antes do commit

        for item in data['itens']:
            novo_item = NotaFiscalItem(
                nota_fiscal_id=nota.id,
                produto_id=item['produto_id'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco_unitario']  # <-- nome correto do campo
            )
            db.session.add(novo_item)

        db.session.commit()
        return jsonify({"mensagem": "Nota fiscal salva com sucesso!"}), 201

    return render_template('nfe_compra.html')

@app.route('/nfe_lista')
def nfe_lista():
    notas = NotaFiscalCompra.query.order_by(NotaFiscalCompra.data_emissao.desc()).all()
    return render_template('nfe_lista.html', notas=notas)

@app.route('/nota_fiscal_venda', methods=['GET', 'POST'])
def nota_fiscal_venda():
    if request.method == 'POST':
        data = request.get_json()

        nota = NotaFiscalVenda(
            numero=data['numero'],
            serie=data['serie'],
            data_emissao=data['data_emissao'],
            cliente_id=data['cliente_id'],
            valor_total=data['valor_total']
        )
        db.session.add(nota)
        db.session.flush()  # Para obter o ID da nota antes do commit

        for item in data['itens']:
            novo_item = NotaFiscalVendaItem(
                nota_fiscal_id=nota.id,
                produto_id=item['produto_id'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco_unitario']  # <-- nome correto do campo
            )
            db.session.add(novo_item)

        db.session.commit()
        return jsonify({"mensagem": "Nota fiscal salva com sucesso!"}), 201

    return render_template('nfe_venda.html')

@app.route('/nfe_lista_venda')
def nfe_lista_venda():
    notas = NotaFiscalVenda.query.order_by(NotaFiscalVenda.data_emissao.desc()).all()
    return render_template('nfe_lista_venda.html', notas=notas)

@app.route('/clientes_json', methods=['GET'])
def clientes_json():
    clientes = Fornecedor.query.with_entities(Cliente.id, Cliente.nome).all()
    return jsonify([{"id": f.id, "nome": f.nome} for f in clientes])

if __name__ == '__main__':
    app.run(debug=True)
