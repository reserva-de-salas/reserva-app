from flask import Flask, render_template

app = Flask(__name__, template_folder="../templates")


@app.route("/")
def home():
    return render_template("cadastrar-sala.html")

@app.route("/cadastrar-sala")
def cadastrar_sala():
    return render_template("cadastrar-sala.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/listar-salas")
def listar_salas():
    return render_template("listar-salas.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/reservar-sala")
def reservar_sala():
    return render_template("reservar-sala.html")

@app.route("/reservas")
def reervas():
    return render_template("reservas.html")



app.run()