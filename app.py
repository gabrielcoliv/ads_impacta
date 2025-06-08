from flask import Flask, request, jsonify, render_template, send_from_directory
from config import SQLALCHEMY_DATABASE_URI
from extensions import db
from models import Empresa, Fornecedor, Produto, Cliente, NotaFiscalCompra, NotaFiscalItem, NotaFiscalVenda, NotaFiscalVendaItem, Estoque
from sqlalchemy.exc import IntegrityError

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

# --- Empresa ---

@app.route('/empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    if request.method == 'POST':
        dados = request.get_json()
        try:
            nova_empresa = Empresa(
                nome=dados['nome'],
                cnpj=dados['cnpj'],
                endereco=dados.get('endereco', ''),
                telefone=dados.get('telefone', ''),
                email=dados.get('email', '')
            )
            db.session.add(nova_empresa)
            db.session.commit()
            return jsonify({"mensagem": "Empresa cadastrada com sucesso!"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"erro": "CNPJ ou email já cadastrado"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": str(e)}), 400
    return render_template('empresa.html')

@app.route('/empresas', methods=['GET'])
def listar_empresas():
    empresas = Empresa.query.all()
    return render_template('consultar_empresas.html', empresas=empresas)

# --- Fornecedor ---

@app.route('/fornecedor', methods=['GET', 'POST'])
def cadastro_fornecedor():
    if request.method == 'POST':
        dados = request.get_json()
        try:
            novo_fornecedor = Fornecedor(
                nome=dados['nome'],
                cnpj=dados['cnpj'],
                telefone=dados.get('telefone', ''),
                email=dados.get('email', '')
            )
            db.session.add(novo_fornecedor)
            db.session.commit()
            return jsonify({"mensagem": "Fornecedor cadastrado com sucesso!"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"erro": "CNPJ ou email já cadastrado"}), 400
        except Exception as e:
            db.session.rollback()
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

# --- Produto ---

@app.route('/produto', methods=['GET', 'POST'])
def cadastro_produto():
    if request.method == 'POST':
        dados = request.get_json()
        try:
            novo_produto = Produto(
                nome=dados['nome'],
                descricao=dados.get('descricao', ''),
                preco=dados['preco'],
                fornecedor_id=dados['fornecedor_id']
            )
            db.session.add(novo_produto)
            db.session.flush()  # para gerar ID do produto antes do estoque

            estoque_inicial = dados.get('estoque', 0)
            novo_estoque = Estoque(produto_id=novo_produto.id, quantidade=estoque_inicial)
            db.session.add(novo_estoque)

            db.session.commit()
            return jsonify({"mensagem": "Produto cadastrado com sucesso!"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"erro": "Erro de integridade, verifique os dados"}), 400
        except Exception as e:
            db.session.rollback()
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

# --- Cliente ---

@app.route('/cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        dados = request.get_json()
        try:
            novo_cliente = Cliente(
                nome=dados['nome'],
                cpf=dados['cpf'],
                telefone=dados.get('telefone', ''),
                email=dados.get('email', '')
            )
            db.session.add(novo_cliente)
            db.session.commit()
            return jsonify({"mensagem": "Cliente cadastrado com sucesso!"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"erro": "CPF ou email já cadastrado"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": str(e)}), 400
    return render_template('cliente.html')

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('consultar_clientes.html', clientes=clientes)

@app.route('/clientes_json', methods=['GET'])
def clientes_json():
    clientes = Cliente.query.with_entities(Cliente.id, Cliente.nome).all()
    return jsonify([{"id": c.id, "nome": c.nome} for c in clientes])

# --- Nota Fiscal Compra ---

@app.route('/nota_fiscal_compra', methods=['GET', 'POST'])
def nota_fiscal_compra():
    if request.method == 'POST':
        dados = request.get_json()
        try:
            nova_nota = NotaFiscalCompra(
                numero=dados['numero'],
                serie=dados.get('serie'),
                data_emissao=dados['data_emissao'],
                fornecedor_id=dados['fornecedor_id'],
                valor_total=dados['valor_total']
            )
            db.session.add(nova_nota)
            db.session.flush()  # gera id antes dos itens

            for item in dados['itens']:
                novo_item = NotaFiscalItem(
                    nota_fiscal_id=nova_nota.id,
                    produto_id=item['produto_id'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco_unitario']
                )
                db.session.add(novo_item)

                estoque = Estoque.query.filter_by(produto_id=item['produto_id']).first()
                if estoque:
                    estoque.quantidade += item['quantidade']
                else:
                    estoque = Estoque(produto_id=item['produto_id'], quantidade=item['quantidade'])
                    db.session.add(estoque)

            db.session.commit()
            return jsonify({"mensagem": "Nota fiscal de compra cadastrada com sucesso!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": str(e)}), 400

    fornecedores = Fornecedor.query.all()
    produtos = Produto.query.all()
    return render_template('nfe_compra.html', fornecedores=fornecedores, produtos=produtos)

@app.route('/notas_fiscais_compra', methods=['GET'])
def listar_notas_fiscais_compra():
    notas = NotaFiscalCompra.query.order_by(NotaFiscalCompra.data_emissao.desc()).all()
    return render_template('consultar_notas_fiscais_compra.html', notas=notas)

@app.route('/nfe_lista')
def nfe_lista():
    notas = NotaFiscalCompra.query.order_by(NotaFiscalCompra.data_emissao.desc()).all()
    return render_template('nfe_lista.html', notas=notas)

# --- Nota Fiscal Venda ---

@app.route('/nota_fiscal_venda', methods=['GET', 'POST'])
def nota_fiscal_venda():
    if request.method == 'POST':
        dados = request.get_json()
        try:
            nova_nota = NotaFiscalVenda(
                numero=dados['numero'],
                serie=dados.get('serie'),
                data_emissao=dados['data_emissao'],
                cliente_id=dados['cliente_id'],
                valor_total=dados['valor_total']
            )
            db.session.add(nova_nota)
            db.session.flush()

            for item in dados['itens']:
                estoque = Estoque.query.filter_by(produto_id=item['produto_id']).first()
                if not estoque or estoque.quantidade < item['quantidade']:
                    db.session.rollback()
                    return jsonify({"erro": f"Estoque insuficiente para o produto {item['produto_id']}"}), 400

                novo_item = NotaFiscalVendaItem(
                    nota_fiscal_id=nova_nota.id,
                    produto_id=item['produto_id'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco_unitario']
                )
                db.session.add(novo_item)

                estoque.quantidade -= item['quantidade']

            db.session.commit()
            return jsonify({"mensagem": "Nota fiscal de venda cadastrada com sucesso!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": str(e)}), 400

    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template('nfe_venda.html', clientes=clientes, produtos=produtos)

@app.route('/notas_fiscais_venda', methods=['GET'])
def listar_notas_fiscais_venda():
    notas = NotaFiscalVenda.query.order_by(NotaFiscalVenda.data_emissao.desc()).all()
    return render_template('consultar_notas_fiscais_venda.html', notas=notas)

@app.route('/nfe_lista_venda')
def nfe_lista_venda():
    notas = NotaFiscalVenda.query.order_by(NotaFiscalVenda.data_emissao.desc()).all()
    return render_template('nfe_lista_venda.html', notas=notas)

@app.route('/estoque', methods=['GET'])
def consultar_estoque():
    # Faz um join do estoque com o produto para mostrar nome e quantidade
    estoque_produtos = db.session.query(
        Produto.nome,
    	Produto.descricao,
    	Estoque.quantidade.label('quantidade_estoque')
    ).join(Estoque, Produto.id == Estoque.produto_id).all()
    return render_template('estoque.html', estoque=estoque_produtos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
