from models import db, Produto, Nota, ItemNota, Movimentacao, Pedido, ItemPedido, Venda, ItemVenda
from datetime import datetime, timedelta
import random
import uuid

# ============ LIMPAR TABELAS ============
db.session.query(ItemVenda).delete()
db.session.query(Venda).delete()
db.session.query(ItemPedido).delete()
db.session.query(Pedido).delete()
db.session.query(Movimentacao).delete()
db.session.query(ItemNota).delete()
db.session.query(Nota).delete()
db.session.query(Produto).delete()
db.session.commit()
print("🧹 Tabelas limpas com sucesso!")

# ============ PRODUTOS ============
produtos_data = [
    ("001", "Pastilha de Freio Dianteira", "Bosch", "Fiat Palio 1.0/1.4", 85.00, 130.00, 40),
    ("002", "Filtro de Ar", "Fram", "Volkswagen Gol G5/G6", 25.00, 45.00, 55),
    ("003", "Correia Dentada", "Dayco", "Chevrolet Onix 1.0", 50.00, 85.00, 30),
    ("004", "Amortecedor Traseiro", "Cofap", "Honda Civic 2016+", 150.00, 230.00, 20),
    ("005", "Velas de Ignição", "NGK", "Ford Ka 1.5", 20.00, 35.00, 80),
    ("006", "Bateria Moura 60Ah", "Moura", "Universal", 350.00, 520.00, 15),
    ("007", "Sensor de Temperatura", "Delphi", "Chevrolet Corsa", 35.00, 60.00, 50),
    ("008", "Disco de Freio", "TRW", "Fiat Uno 1.0/1.4", 95.00, 140.00, 25),
    ("009", "Filtro de Combustível", "Tecfil", "Chevrolet Prisma", 20.00, 38.00, 60),
    ("010", "Kit Embreagem", "Sachs", "Volkswagen Fox 1.6", 280.00, 420.00, 10),
]
produtos = [Produto(codigo=c, descricao=d, marca=m, aplicacao=a,
                    preco_compra=pc, preco_venda=pv, estoque_atual=e)
            for c, d, m, a, pc, pv, e in produtos_data]
db.session.add_all(produtos)
db.session.commit()
print(f"✅ {len(produtos)} produtos inseridos!")

# ============ NOTAS FISCAIS + ITENS ============
notas = []
for i in range(10):
    nota = Nota(
        numero=f"NF-{100+i}",
        fornecedor=random.choice(["Auto Peças Brasil", "Distribuidora XYZ", "Supreme Parts", "MecParts Ltda"]),
        data=datetime.now() - timedelta(days=random.randint(5, 30)),
        valor_total=0.0,
        chave_acesso=str(uuid.uuid4())
    )
    db.session.add(nota)
    notas.append(nota)
db.session.commit()

itens_notas = []
for nota in notas:
    total = 0
    for _ in range(random.randint(2, 4)):
        produto = random.choice(produtos)
        qtd = random.randint(5, 15)
        preco = produto.preco_compra
        subtotal = qtd * preco
        total += subtotal

        itens_notas.append(ItemNota(
            nota_id=nota.id,
            produto_id=produto.id,
            quantidade=qtd,
            preco_unitario=preco,
            subTotal=subtotal
        ))

        db.session.add(Movimentacao(
            produto_id=produto.id,
            tipo="entrada",
            quantidade=qtd,
            data=nota.data
        ))

    nota.valor_total = total

db.session.add_all(itens_notas)
db.session.commit()
print(f"✅ {len(notas)} notas e {len(itens_notas)} itens de notas inseridos!")

# ============ MOVIMENTAÇÕES DE SAÍDA ============
for _ in range(20):
    produto = random.choice(produtos)
    qtd = random.randint(1, 10)
    db.session.add(Movimentacao(
        produto_id=produto.id,
        tipo="saida",
        quantidade=qtd,
        data=datetime.now() - timedelta(days=random.randint(0, 30))
    ))
db.session.commit()
print("✅ Movimentações de saída geradas!")

# ============ PEDIDOS ENTRE FILIAIS ============
pedidos = []
for i in range(8):
    pedido = Pedido(
        origem=f"Filial {random.choice(['A', 'B', 'C'])}",
        destino=f"Filial {random.choice(['D', 'E', 'F'])}",
        data=datetime.now() - timedelta(days=random.randint(3, 30)),
        status=random.choice(["Pendente", "Enviado", "Recebido"])
    )
    db.session.add(pedido)
    pedidos.append(pedido)
db.session.commit()

itens_pedidos = []
for pedido in pedidos:
    for _ in range(random.randint(2, 4)):
        produto = random.choice(produtos)
        qtd = random.randint(1, 8)
        itens_pedidos.append(ItemPedido(
            pedido_id=pedido.id,
            produto_id=produto.id,
            quantidade=qtd
        ))

db.session.add_all(itens_pedidos)
db.session.commit()
print(f"✅ {len(pedidos)} pedidos e {len(itens_pedidos)} itens de pedidos inseridos!")

# ============ VENDAS ============
clientes = [
    "João da Silva", "Maria Oliveira", "Oficina Rápida Ltda",
    "Auto Mecânica São José", "Carlos Pneus", "Mecânica do Zé",
    "Pedro Peças", "Super Auto Serviços"
]
vendas = []
for i in range(15):
    venda = Venda(
        numero=f"VND-{1000+i}",
        cliente=random.choice(clientes),
        data=datetime.now() - timedelta(days=random.randint(0, 30)),
        valor_total=0.0
    )
    db.session.add(venda)
    vendas.append(venda)
db.session.commit()

itens_vendas = []
for venda in vendas:
    total = 0
    for _ in range(random.randint(2, 5)):
        produto = random.choice(produtos)
        qtd = random.randint(1, 4)
        preco = produto.preco_venda
        subtotal = qtd * preco
        total += subtotal

        itens_vendas.append(ItemVenda(
            venda_id=venda.id,
            produto_id=produto.id,
            quantidade=qtd,
            preco_unitario=preco,
            subTotal=subtotal
        ))

        db.session.add(Movimentacao(
            produto_id=produto.id,
            tipo="saida",
            quantidade=qtd,
            data=venda.data
        ))

    venda.valor_total = total

db.session.add_all(itens_vendas)
db.session.commit()
print(f"✅ {len(vendas)} vendas e {len(itens_vendas)} itens de vendas inseridos!")

print("\n🎉 Base de dados Autopeças populada com histórico de 30 dias!")
