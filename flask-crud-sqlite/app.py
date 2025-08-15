from flask import Flask, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "database.db"

# ======== Banco de dados ========
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(nome, email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id FROM usuarios WHERE email=?", (email,))
    if not cur.fetchone():
        cur.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
        conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    conn.close()
    return usuarios

# ======== Rotas ========
# Página inicial: formulário de cadastro
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        if nome and email:
            add_user(nome, email)
        return redirect("/")

    usuarios = get_all_users()

    html = "<h1>Banco de Usuários</h1>"
    html += """
    <form method='POST'>
        Nome: <input type='text' name='nome' required>
        Email: <input type='email' name='email' required>
        <input type='submit' value='Adicionar'>
    </form>
    <br>
    """
    html += "<table border='1' style='border-collapse: collapse;'>"
    html += "<tr><th>ID</th><th>Nome</th><th>Email</th></tr>"
    for u in usuarios:
        html += f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>"
    html += "</table>"


    return html

# ======== Executar ========
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
