
from flask import Flask, request, redirect
from html import escape

app = Flask(__name__)

pedidos = []
estoque = [
    {"nome": "Farinha de trigo", "quantidade": 2, "minimo": 5},
    {"nome": "Açúcar", "quantidade": 10, "minimo": 3},
    {"nome": "Fermento", "quantidade": 1, "minimo": 4}
]

def pagina(conteudo):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Sabor de Vó</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #faf5ed;
                color: #30251d;
                margin: 0;
            }}
            header {{
                background: #70452e;
                color: white;
                padding: 24px;
                text-align: center;
            }}
            nav {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
                padding: 18px;
            }}
            a, button {{
                background: #70452e;
                color: white;
                padding: 12px 18px;
                border-radius: 8px;
                text-decoration: none;
                border: none;
                cursor: pointer;
                min-height: 44px;
                box-sizing: border-box;
                font-size: 16px;
            }}
            a:focus-visible, button:focus-visible,
            input:focus-visible {{
                outline: 3px solid #0066cc;
                outline-offset: 3px;
            }}
            main {{
                max-width: 850px;
                margin: 20px auto;
                padding: 24px;
                background: white;
                border-radius: 12px;
            }}
            input {{
                padding: 12px;
                margin: 8px 0 16px;
                width: 100%;
                box-sizing: border-box;
                font-size: 16px;
            }}
            label {{ display: block; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{
                padding: 12px;
                border: 1px solid #aaa;
                text-align: left;
            }}
            .alerta {{
                background: #fff0d8;
                border-left: 5px solid #995000;
                padding: 12px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Sabor de Vó</h1>
            <p>Sistema de gerenciamento de pedidos e estoque</p>
        </header>
        <nav aria-label="Menu principal">
            <a href="/">Início</a>
            <a href="/pedidos">Pedidos</a>
            <a href="/estoque">Estoque</a>
        </nav>
        <main>{conteudo}</main>
    </body>
    </html>
    """

@app.route("/")
def inicio():
    return pagina("""
        <h2>Bem-vindo ao Sabor de Vó!</h2>
        <p>Gerencie pedidos e acompanhe os ingredientes da padaria.</p>
        <p>Projeto acadêmico relacionado ao ODS 12:
        Consumo e Produção Responsáveis.</p>
        <p>Utilize o menu para acessar as funcionalidades.</p>
    """)

@app.route("/pedidos", methods=["GET", "POST"])
def gerenciar_pedidos():
    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        produto = request.form.get("produto", "").strip()
        if cliente and produto:
            pedidos.append({"cliente": cliente, "produto": produto})
        return redirect("/pedidos")

    linhas = "".join(
        f"<tr><td>{escape(p['cliente'])}</td>"
        f"<td>{escape(p['produto'])}</td>"
        "<td>Pendente</td></tr>"
        for p in pedidos
    )

    return pagina(f"""
        <h2>Gerenciamento de Pedidos</h2>
        <form method="POST">
            <label for="cliente">Nome do cliente</label>
            <input id="cliente" name="cliente" required>

            <label for="produto">Produto solicitado</label>
            <input id="produto" name="produto" required>

            <button type="submit">Cadastrar pedido</button>
        </form>
        <h3>Pedidos cadastrados</h3>
        <table>
            <tr><th>Cliente</th><th>Produto</th><th>Status</th></tr>
            {linhas}
        </table>
    """)

@app.route("/estoque", methods=["GET", "POST"])
def gerenciar_estoque():
    if request.method == "POST":
        nome = request.form.get("ingrediente", "").strip()
        try:
            quantidade = float(request.form.get("quantidade", "0"))
            minimo = float(request.form.get("minimo", "0"))
        except ValueError:
            quantidade, minimo = -1, -1

        if nome and quantidade >= 0 and minimo >= 0:
            estoque.append({
                "nome": nome,
                "quantidade": quantidade,
                "minimo": minimo
            })
        return redirect("/estoque")

    linhas = ""
    for item in estoque:
        baixo = item["quantidade"] <= item["minimo"]
        estado = "⚠ Estoque baixo" if baixo else "✓ Adequado"
        linhas += (
            f"<tr><td>{escape(item['nome'])}</td>"
            f"<td>{item['quantidade']:g}</td>"
            f"<td>{item['minimo']:g}</td>"
            f"<td>{estado}</td></tr>"
        )

    return pagina(f"""
        <h2>Controle de Estoque</h2>
        <p class="alerta">⚠ Verifique os ingredientes
        sinalizados com estoque baixo.</p>

        <table>
            <tr><th>Ingrediente</th><th>Quantidade</th>
            <th>Mínimo</th><th>Situação</th></tr>
            {linhas}
        </table>

        <h3>Cadastrar ingrediente</h3>
        <form method="POST">
            <label for="ingrediente">Ingrediente</label>
            <input id="ingrediente" name="ingrediente" required>

            <label for="quantidade">Quantidade atual</label>
            <input id="quantidade" name="quantidade"
                   type="number" min="0" step="0.01" required>

            <label for="minimo">Estoque mínimo</label>
            <input id="minimo" name="minimo"
                   type="number" min="0" step="0.01" required>

            <button type="submit">Salvar ingrediente</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)
