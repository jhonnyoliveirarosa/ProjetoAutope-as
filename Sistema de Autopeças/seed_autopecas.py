from models import db, Produto, Nota, ItemNota, Movimentacao
from datetime import datetime, timedelta
import random

# ====== LISTA DE PRODUTOS (20 PEÇAS REAIS DE AUTOPEÇAS) ======
produtos = [
    ("001", "Pastilha de Freio Dianteira", "Bosch", "Chevrolet Onix", 85.00, 135.00, 25),
    ("002", "Filtro de Óleo", "Fram", "Fiat Strada", 20.00, 35.00, 40),
    ("003", "Amortecedor Traseiro", "Cofap", "Gol G6", 210.00, 330.00, 15),
    ("004", "Vela de Ignição", "NGK", "Uno 1.0", 15.00, 28.00, 50),
    ("005", "Correia Dentada", "Dayco", "HB20 1.6", 60.00, 100.00, 30),
    ("006", "Bateria 60Ah", "Moura", "Universal", 350.00, 550.00, 10),
    ("007", "Farol Dianteiro Direito", "Arteb", "Corolla 2018", 440.00, 690.00, 8),
    ("008", "Filtro de Ar", "Tecfil", "Fiesta 1.6", 28.00, 45.00, 35),
    ("009", "Disco de Freio", "Fremax", "Civic 2016", 190.00, 290.00, 18),
    ("010", "Bucha de Bandeja", "Nakata", "Palio", 25.00, 45.00, 40),
    ("011", "Rolamento de Roda", "SKF", "Gol G7", 120.00, 200.00, 22),
    ("012", "Sensor de ABS", "Delphi", "Corolla 2019", 130.00, 210.00, 12),
    ("013", "Cabo de Vela", "NGK", "Corsa", 55.00, 95.00, 25),
    ("014", "Filtro de Combustível", "Mann", "Sandero", 35.00, 58.00, 28),
    ("015", "Lâmpada H7", "Osram", "Universal", 18.00, 35.00, 40),
    ("016", "Embreagem Completa", "Sachs", "Fox 1.6", 380.00, 580.00, 9),
    ("017", "Radiador", "Valeo", "Civic 2015", 420.00, 670.00, 6),
    ("018", "Bico Injetor", "Bosch", "HB20 1.0", 160.00, 250.00, 16),
    ("019", "Coxim do Motor", "Spicer", "Celta 1.4", 85.00, 130.00, 20),
    ("020", "Parachoque Dianteiro", "Plascar", "Onix 2020", 390.00, 650.00, 5),
]

# Inserir produtos no banco
prod_objs = []
for p in produtos:
    prod = Produto(
        codigo=p[0],
        descricao=p[1],
        marca=p[2],
        aplicacao=p[3],
        preco_compra=p[4],
        preco_venda=p[5],
        estoque_atual=p[6],
    )
    prod_objs.append(prod)

db.session.add_all(prod_objs)
db.session.commit()

print(f"✅ {len(prod_objs)} produtos inseridos com sucesso!")


# ====== NOTAS FISCAIS DE EXEMPLO ======
nota1 = Nota(numero="NF-2025-001", fornecedor="Autopeças Brasil Ltda", data=datetime(2025, 11, 5), valor_total=0.0)
nota2 = Nota(numero="NF-2025-002", fornecedor="Distribuidora São Paulo", data=datetime(2025, 11, 10), valor_total=0.0)

db.session.add_all([nota1, nota2])
db.session.commit()

# ====== ITENS DAS NOTAS ======
itens = [
    ItemNota(nota_id=nota1.id, produto_id=prod_objs[0].id, quantidade=10, preco_unitario=85.00, subTotal=850.00),
    ItemNota(nota_id=nota1.id, produto_id=prod_objs[1].id, quantidade=20, preco_unitario=20.00, subTotal=400.00),
    ItemNota(nota_id=nota2.id, produto_id=prod_objs[3].id, quantidade=30, preco_unitario=15.00, subTotal=450.00),
    ItemNota(nota_id=nota2.id, produto_id=prod_objs[5].id, quantidade=5, preco_unitario=350.00, subTotal=1750.00),
]

nota1.valor_total = sum([i.subTotal for i in itens if i.nota_id == nota1.id])
nota2.valor_total = sum([i.subTotal for i in itens if i.nota_id == nota2.id])

db.session.add_all(itens)
db.session.commit()

print("✅ Notas fiscais e itens inseridos com sucesso!")


# ====== MOVIMENTAÇÕES ======
movs = []
tipos = ["Entrada", "Saida"]
for i in range(30):
    produto = random.choice(prod_objs)
    tipo = random.choice(tipos)
    qtd = random.randint(2, 40)
    dias_atras = random.randint(0, 10)
    data_mov = datetime.now() - timedelta(days=dias_atras)
    movs.append(Movimentacao(produto_id=produto.id, tipo=tipo, quantidade=qtd, data=data_mov))

db.session.add_all(movs)
db.session.commit()

print(f"✅ {len(movs)} movimentações geradas aleatoriamente!")
