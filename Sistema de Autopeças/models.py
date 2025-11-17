from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


# =========================================================
# PRODUTO
# =========================================================
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50))
    aplicacao = db.Column(db.String(100))
    preco_compra = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    estoque_atual = db.Column(db.Integer, default=0)

    itens = db.relationship("ItemNota", backref="produto", lazy=True)
    movimentacoes = db.relationship("Movimentacao", backref="produto", lazy=True)

    def __repr__(self):
        return f"<Produto {self.descricao}>"


# =========================================================
# NOTA FISCAL
# =========================================================
class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)
    fornecedor = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)

    chave_acesso = db.Column(
        db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    itens = db.relationship("ItemNota", backref="nota", lazy=True)

    def __repr__(self):
        return f"<Nota {self.numero}>"


class ItemNota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota_id = db.Column(db.Integer, db.ForeignKey("nota.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subTotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<ItemNota {self.nota_id} - {self.quantidade}x>"


# =========================================================
# MOVIMENTAÇÃO
# =========================================================
class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # entrada / saída
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Movimentacao {self.tipo} {self.quantidade}x>"


# =========================================================
# PEDIDOS ENTRE FILIAIS
# =========================================================
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origem = db.Column(db.String(50), nullable=False)
    destino = db.Column(db.String(50), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(
        db.String(20), default="Pendente"
    )  # Pendente / Enviado / Recebido

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)

    def __repr__(self):
        return f"<Pedido {self.id} - {self.origem} → {self.destino}>"


class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    produto = db.relationship("Produto")

    def __repr__(self):
        return f"<ItemPedido {self.produto.descricao} x{self.quantidade}>"


# =========================================================
# VENDAS
# =========================================================
class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Float, default=0.0)
    nota_id = db.Column(db.Integer, db.ForeignKey("nota.id"), nullable=True)

    itens = db.relationship("ItemVenda", backref="venda", lazy=True)

    def __repr__(self):
        return f"<Venda {self.numero} - {self.cliente}>"


class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey("venda.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subTotal = db.Column(db.Float, nullable=False)

    produto = db.relationship("Produto")

    def __repr__(self):
        return f"<ItemVenda {self.produto.descricao} ({self.quantidade}x)>"


# =========================================================
# CLIENTES
# =========================================================
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cnpj = db.Column(db.String(25))
    endereco = db.Column(db.String(200))

    def __repr__(self):
        return f"<Cliente {self.nome}>"
