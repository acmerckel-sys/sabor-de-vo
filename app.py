
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return """
    <h1>Sabor de Vó</h1>
    <p>Sistema de gerenciamento de pedidos e estoque.</p>
    <p>Projeto acadêmico de Análise e Desenvolvimento de Sistemas.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
