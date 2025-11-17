from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from functools import wraps
import os

# Importa os modelos
from models import (
    db,
    Produto,
    Nota,
    ItemNota,
    Movimentacao,
    Pedido,
    ItemPedido,
    ItemVenda,
    Venda,
    Cliente,
)

# === Configuração inicial ===
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.urandom(24)
db.init_app(app)


# === Context processor: disponibiliza variáveis para todos os templates ===
@app.context_processor
def inject_globals():
    return {
        "current_year": datetime.now().year,
        "user": session.get("user"),
    }


# === Sistema de Login / decorator ===
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("username", "").strip()
        senha = request.form.get("password", "")

        # aqui você pode trocar por validação real no DB
        if usuario == "admin" and senha == "1234":
            session["user"] = usuario
            flash("Login efetuado com sucesso.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuário ou senha incorretos.", "error")
            return redirect(url_for("login"))

    # GET
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Você saiu do sistema.")
    return redirect(url_for("login"))


# === Rotas protegidas ===
@app.route("/")
@login_required
def home():
    return redirect(url_for("dashboard"))


# ---------------- PRODUTOS ----------------
@app.route("/produtos", methods=["GET", "POST"])
@login_required
def produtos():
    if request.method == "POST":
        try:
            codigo = request.form["codigo"]
            descricao = request.form["descricao"]
            marca = request.form.get("marca")
            aplicacao = request.form.get("aplicacao")
            preco_compra = float(request.form["preco_compra"] or 0)
            preco_venda = float(request.form["preco_venda"] or 0)

            novo = Produto(
                codigo=codigo,
                descricao=descricao,
                marca=marca,
                aplicacao=aplicacao,
                preco_compra=preco_compra,
                preco_venda=preco_venda,
            )
            db.session.add(novo)
            db.session.commit()
            flash("Produto cadastrado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar produto: {e}", "error")
        return redirect(url_for("produtos"))

    lista = Produto.query.all()
    return render_template("pages/produtos/produtos.html", produtos=lista)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    produto = Produto.query.get_or_404(id)
    if request.method == "POST":
        try:
            produto.codigo = request.form["codigo"]
            produto.descricao = request.form["descricao"]
            produto.marca = request.form.get("marca")
            produto.aplicacao = request.form.get("aplicacao")
            produto.preco_compra = float(request.form["preco_compra"] or 0)
            produto.preco_venda = float(request.form["preco_venda"] or 0)
            db.session.commit()
            flash("Produto editado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao editar produto: {e}", "error")
        return redirect(url_for("produtos"))
    return render_template("pages/produtos/editar.html", produto=produto)


@app.route("/excluir/<int:id>")
@login_required
def excluir(id):
    produto = Produto.query.get_or_404(id)
    try:
        db.session.delete(produto)
        db.session.commit()
        flash("Produto excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir produto: {e}", "error")
    return redirect(url_for("produtos"))


# ---------------- NOTAS ----------------
@app.route("/notas", methods=["GET", "POST"])
@login_required
def notas():
    if request.method == "POST":
        try:
            numero = request.form["numero"]
            fornecedor = request.form["fornecedor"]
            data_string = request.form["data"]
            valor_total = float(request.form.get("valor_total") or 0)
            data = datetime.strptime(data_string, "%Y-%m-%d").date()

            nova_nota = Nota(
                numero=numero, fornecedor=fornecedor, data=data, valor_total=valor_total
            )
            db.session.add(nova_nota)
            db.session.commit()
            flash("Nota cadastrada com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar nota: {e}", "error")
        return redirect(url_for("notas"))

    lista = Nota.query.all()
    return render_template("pages/notas/notas.html", notas=lista)


@app.route("/editar_nota/<int:id>", methods=["GET", "POST"])
@login_required
def editar_nota(id):
    nota = Nota.query.get_or_404(id)
    if request.method == "POST":
        try:
            nota.numero = request.form["numero"]
            nota.fornecedor = request.form["fornecedor"]
            nota.data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
            nota.valor_total = float(request.form.get("valor_total") or 0)
            db.session.commit()
            flash("Nota atualizada com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar nota: {e}", "error")
        return redirect(url_for("notas"))
    return render_template("pages/notas/editar.html", nota=nota)


@app.route("/excluir_nota/<int:id>")
@login_required
def excluir_nota(id):
    nota = Nota.query.get_or_404(id)
    try:
        db.session.delete(nota)
        db.session.commit()
        flash("Nota excluída com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir nota: {e}", "error")
    return redirect(url_for("notas"))


@app.route("/itens/<int:nota_id>", methods=["GET", "POST"])
@login_required
def itens_nota(nota_id):
    nota = Nota.query.get_or_404(nota_id)
    produtos = Produto.query.all()

    if request.method == "POST":
        try:
            produto_id = int(request.form["produto_id"])
            quantidade = int(request.form["quantidade"])
            preco_unitario = float(request.form["preco_unitario"])
            subTotal = quantidade * preco_unitario

            novo_item = ItemNota(
                nota_id=nota.id,
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subTotal=subTotal,
            )
            db.session.add(novo_item)

            produto = Produto.query.get(produto_id)
            produto.estoque_atual = (produto.estoque_atual or 0) + quantidade

            mov = Movimentacao(
                produto_id=produto_id, tipo="entrada", quantidade=quantidade
            )
            db.session.add(mov)

            # atualiza total da nota (usar itens atuais + novo item)
            db.session.flush()  # garante que novo_item esteja visível na sessão
            nota.valor_total = sum(i.subTotal for i in nota.itens)  # inclui novo_item
            db.session.commit()
            flash("Item adicionado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao adicionar item: {e}", "error")

        return redirect(url_for("itens_nota", nota_id=nota.id))

    itens = ItemNota.query.filter_by(nota_id=nota.id).all()
    return render_template("pages/notas/itens.html", nota=nota, produtos=produtos, itens=itens)


# ---------------- ESTOQUE ----------------
@app.route("/estoque")
@login_required
def estoque():
    produtos = Produto.query.all()
    return render_template("pages/estoque/estoque.html", produtos=produtos)


# ---------------- MOVIMENTAÇÕES ----------------
@app.route("/movimentacoes", methods=["GET", "POST"])
@login_required
def movimentacoes():
    produtos = Produto.query.all()

    if request.method == "POST":
        try:
            produto_id = int(request.form["produto_id"])
            tipo = request.form["tipo"]
            quantidade = int(request.form["quantidade"])

            nova_mov = Movimentacao(
                produto_id=produto_id, tipo=tipo, quantidade=quantidade
            )
            db.session.add(nova_mov)

            produto = Produto.query.get(produto_id)
            if tipo == "entrada":
                produto.estoque_atual = (produto.estoque_atual or 0) + quantidade
            else:
                produto.estoque_atual = (produto.estoque_atual or 0) - quantidade

            db.session.commit()
            flash("Movimentação registrada com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao registrar movimentação: {e}", "error")
        return redirect(url_for("movimentacoes"))

    lista = Movimentacao.query.order_by(Movimentacao.data.desc()).all()
    return render_template(
        "pages/movimentacoes/movimentacoes.html", movimentacoes=lista, produtos=produtos
    )


# ---------------- PEDIDOS ----------------
@app.route("/pedidos", methods=["GET", "POST"])
@login_required
def pedidos():
    if request.method == "POST":
        try:
            origem = request.form["origem"]
            destino = request.form["destino"]
            novo = Pedido(origem=origem, destino=destino)
            db.session.add(novo)
            db.session.commit()
            flash("Pedido criado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar pedido: {e}", "error")
        return redirect(url_for("pedidos"))

    lista = Pedido.query.order_by(Pedido.data.desc()).all()
    return render_template("pages/pedidos/pedidos.html", pedidos=lista)


@app.route("/itens_pedido/<int:pedido_id>", methods=["GET", "POST"])
@login_required
def itens_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    produtos = Produto.query.all()

    if request.method == "POST":
        try:
            produto_id = int(request.form["produto_id"])
            quantidade = int(request.form["quantidade"])
            produto = Produto.query.get(produto_id)

            if produto.estoque_atual < quantidade:
                flash(f"Estoque insuficiente para {produto.descricao}.", "error")
                return redirect(url_for("itens_pedido", pedido_id=pedido.id))

            item = ItemPedido(
                pedido_id=pedido.id, produto_id=produto_id, quantidade=quantidade
            )
            db.session.add(item)
            produto.estoque_atual -= quantidade
            mov = Movimentacao(produto_id=produto.id, tipo="saida", quantidade=quantidade)
            db.session.add(mov)
            db.session.commit()

            flash("Item adicionado ao pedido e estoque atualizado!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao adicionar item ao pedido: {e}", "error")

        return redirect(url_for("itens_pedido", pedido_id=pedido.id))

    itens = ItemPedido.query.filter_by(pedido_id=pedido.id).all()
    return render_template(
        "pages/pedidos/itens.html", pedido=pedido, produtos=produtos, itens=itens
    )


@app.route("/receber_pedido/<int:id>")
@login_required
def receber_pedido(id):
    pedido = Pedido.query.get_or_404(id)

    if pedido.status != "Recebido":
        try:
            itens = ItemPedido.query.filter_by(pedido_id=pedido.id).all()
            for item in itens:
                produto = Produto.query.get(item.produto_id)
                produto.estoque_atual = (produto.estoque_atual or 0) + item.quantidade
                mov = Movimentacao(
                    produto_id=produto.id, tipo="entrada", quantidade=item.quantidade
                )
                db.session.add(mov)
            pedido.status = "Recebido"
            db.session.commit()
            flash("Pedido recebido com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao receber pedido: {e}", "error")
    else:
        flash("Este pedido já foi recebido.")

    return redirect(url_for("pedidos"))


# ---------------- BUSCA AJAX ----------------
@app.route("/buscar_produtos")
@login_required
def buscar_produtos():
    termo = request.args.get("q", "").strip()
    produtos = Produto.query.filter(Produto.descricao.ilike(f"%{termo}%")).all()
    resultados = [
        {"id": p.id, "text": f"{p.codigo} - {p.descricao} ({p.marca or ''})"}
        for p in produtos
    ]
    return jsonify(resultados)


# ---------------- VENDAS ----------------
@app.route("/vendas", methods=["GET", "POST"])
@login_required
def vendas():
    if request.method == "POST":
        try:
            numero = request.form["numero"]
            cliente = request.form["cliente"]
            data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
            nova = Venda(numero=numero, cliente=cliente, data=data, valor_total=0)
            db.session.add(nova)
            db.session.commit()
            flash("Venda cadastrada com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar venda: {e}", "error")
        return redirect(url_for("vendas"))

    lista = Venda.query.order_by(Venda.data.desc()).all()
    return render_template("pages/vendas/vendas.html", vendas=lista)


@app.route("/itens_venda/<int:venda_id>", methods=["GET", "POST"])
@login_required
def itens_venda(venda_id):
    venda = Venda.query.get_or_404(venda_id)
    produtos = Produto.query.all()

    if request.method == "POST":
        try:
            produto_id = int(request.form["produto_id"])
            quantidade = int(request.form["quantidade"])
            preco_unitario = float(request.form["preco_unitario"])
            subTotal = quantidade * preco_unitario

            produto = Produto.query.get(produto_id)
            if produto.estoque_atual < quantidade:
                flash(f"Estoque insuficiente para {produto.descricao}.", "error")
                return redirect(url_for("itens_venda", venda_id=venda.id))

            item = ItemVenda(
                venda_id=venda.id,
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subTotal=subTotal,
            )
            db.session.add(item)
            produto.estoque_atual -= quantidade
            db.session.add(
                Movimentacao(produto_id=produto_id, tipo="saida", quantidade=quantidade)
            )

            db.session.flush()
            venda.valor_total = sum(i.subTotal for i in venda.itens)
            db.session.commit()
            flash("Item adicionado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao adicionar item: {e}", "error")
        return redirect(url_for("itens_venda", venda_id=venda.id))

    itens = ItemVenda.query.filter_by(venda_id=venda.id).all()
    return render_template(
        "pages/vendas/itens.html", venda=venda, produtos=produtos, itens=itens
    )


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    mes_atual = int(request.args.get("mes", datetime.now().month))
    ano_atual = int(request.args.get("ano", datetime.now().year))

    anos_disponiveis = [
        int(r[0])
        for r in db.session.query(func.strftime("%Y", Movimentacao.data))
        .distinct()
        .all()
        if r[0]
    ] or [ano_atual]

    vendas_mes = (
        db.session.query(func.sum(Venda.valor_total))
        .filter(
            func.strftime("%m", Venda.data) == f"{mes_atual:02}",
            func.strftime("%Y", Venda.data) == str(ano_atual),
        )
        .scalar()
        or 0
    )

    entradas_mes = (
        db.session.query(func.sum(Movimentacao.quantidade))
        .filter(
            func.strftime("%m", Movimentacao.data) == f"{mes_atual:02}",
            func.strftime("%Y", Movimentacao.data) == str(ano_atual),
            Movimentacao.tipo == "entrada",
        )
        .scalar()
        or 0
    )

    saidas_mes = (
        db.session.query(func.sum(Movimentacao.quantidade))
        .filter(
            func.strftime("%m", Movimentacao.data) == f"{mes_atual:02}",
            func.strftime("%Y", Movimentacao.data) == str(ano_atual),
            Movimentacao.tipo == "saida",
        )
        .scalar()
        or 0
    )

    entradas_total = (
        db.session.query(func.sum(Movimentacao.quantidade))
        .filter(
            func.strftime("%m", Movimentacao.data) == f"{mes_atual:02}",
            func.strftime("%Y", Movimentacao.data) == str(ano_atual),
            Movimentacao.tipo == "entrada",
        )
        .scalar()
        or 0
    )

    saidas_total = (
        db.session.query(func.sum(Movimentacao.quantidade))
        .filter(
            func.strftime("%m", Movimentacao.data) == f"{mes_atual:02}",
            func.strftime("%Y", Movimentacao.data) == str(ano_atual),
            Movimentacao.tipo == "saida",
        )
        .scalar()
        or 0
    )

    produtos_criticos = Produto.query.filter(Produto.estoque_atual < 5).all()
    valor_estoque = (
        db.session.query(func.sum(Produto.estoque_atual * Produto.preco_venda)).scalar()
        or 0
    )

    dias = list(range(1, 32))
    entradas_por_dia = []
    saidas_por_dia = []

    for dia in dias:
        entradas_dia = (
            db.session.query(func.sum(Movimentacao.quantidade))
            .filter(
                func.strftime("%d", Movimentacao.data) == f"{dia:02}",
                func.strftime("%m", Movimentacao.data) == f"{mes_atual:02}",
                func.strftime("%Y", Movimentacao.data) == str(ano_atual),
                Movimentacao.tipo == "entrada",
            )
            .scalar()
            or 0
        )

        saidas_dia = (
            db.session.query(func.sum(Movimentacao.quantidade))
            .filter(
                func.strftime("%d", Movimentacao.data) == f"{dia:02}",
                func.strftime("%m", Movimentacao.data) == f"{mes_atual:02}",
                func.strftime("%Y", Movimentacao.data) == str(ano_atual),
                Movimentacao.tipo == "saida",
            )
            .scalar()
            or 0
        )

        entradas_por_dia.append(entradas_dia)
        saidas_por_dia.append(saidas_dia)

    return render_template(
        "admin/dashboard.html",
        vendas_mes=vendas_mes,
        entradas_mes=entradas_mes,
        saidas_mes=saidas_mes,
        produtos_criticos=produtos_criticos,
        valor_estoque=valor_estoque,
        dias=dias,
        entradas_por_dia=entradas_por_dia,
        saidas_por_dia=saidas_por_dia,
        mes_atual=mes_atual,
        ano_atual=ano_atual,
        anos_disponiveis=anos_disponiveis,
        entradas_total=entradas_total,
        saidas_total=saidas_total,
    )


# ---------------- CLIENTES ----------------
@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():
    if request.method == "POST":
        try:
            nome = request.form.get("nome")
            cnpj = request.form.get("cnpj")
            endereco = request.form.get("endereco")

            novo = Cliente(nome=nome, cnpj=cnpj, endereco=endereco)
            db.session.add(novo)
            db.session.commit()
            flash("Cliente cadastrado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar cliente: {e}", "error")
        return redirect(url_for("clientes"))

    lista = Cliente.query.all()
    return render_template(
        "pages/cliente/clientes.html", clientes=lista, css="cliente.css"
    )


@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":
        try:
            cliente.nome = request.form.get("nome")
            cliente.cnpj = request.form.get("cnpj")
            cliente.endereco = request.form.get("endereco")
            db.session.commit()
            flash("Cliente atualizado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar cliente: {e}", "error")
        return redirect(url_for("clientes"))

    return render_template("pages/cliente/editar.html", cliente=cliente)


@app.route("/clientes/excluir/<int:id>")
@login_required
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash("Cliente removido com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao remover cliente: {e}", "error")
    return redirect(url_for("clientes"))


# === Execução ===
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(f"📦 Banco de dados pronto em: {os.path.abspath('app.db')}")
    app.run(debug=True)
