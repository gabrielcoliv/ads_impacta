from extensions import db

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

    produtos = db.relationship('Produto', backref='fornecedor', lazy='joined')

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)

# ---------- Estoque ----------

class Estoque(db.Model):
    __tablename__ = 'estoque'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False, unique=True)
    quantidade = db.Column(db.Integer, nullable=False, default=0)

    produto = db.relationship('Produto', backref=db.backref('estoque', uselist=False))

# ---------- Notas Fiscais Compra ----------

class NotaFiscalCompra(db.Model):
    __tablename__ = 'compras_notas_fiscais'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)
    serie = db.Column(db.String(10))
    data_emissao = db.Column(db.Date, nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)

    fornecedor = db.relationship('Fornecedor')
    itens = db.relationship('NotaFiscalItem', backref='nota_fiscal', lazy=True)

class NotaFiscalItem(db.Model):
    __tablename__ = 'compras_notas_fiscais_itens'

    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('compras_notas_fiscais.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship('Produto')

# ---------- Notas Fiscais Venda ----------

class NotaFiscalVenda(db.Model):
    __tablename__ = 'vendas_notas_fiscais'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)
    serie = db.Column(db.String(10))
    data_emissao = db.Column(db.Date, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)

    cliente = db.relationship('Cliente')
    itens = db.relationship('NotaFiscalVendaItem', backref='nota_fiscal', lazy=True)

class NotaFiscalVendaItem(db.Model):
    __tablename__ = 'vendas_notas_fiscais_itens'

    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('vendas_notas_fiscais.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship('Produto')
