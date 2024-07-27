from flask import Flask, render_template, redirect, request, flash
import csv
import os

app = Flask(__name__, template_folder="../templates")
app.secret_key = 'sua_chave_secreta'  # Necessário para usar a funcionalidade de mensagens

# Caminhos dos arquivos CSV
salas_csv = "salas.csv"
usuarios_csv = "usuarios.csv"
reservas_csv = "reservas.csv"

# Função para criar o arquivo CSV se ele não existir
def create_csv_file(file_path, headers):
    if not os.path.exists(file_path):
        with open(file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

# Cria os arquivos CSV se eles não existirem
create_csv_file(salas_csv, ["tipo", "capacidade", "descricao", "ativa"])
create_csv_file(usuarios_csv, ["nome", "email", "password"])
create_csv_file(reservas_csv, ["sala", "inicio", "fim"])

# Função para ler salas do arquivo CSV
def ler_salas():
    salas = []
    if os.path.exists(salas_csv):
        with open(salas_csv, "r", newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for idx, linha in enumerate(reader):
                if linha:  # Verifica se a linha não está vazia
                    # Verifica se a linha tem o número esperado de campos
                    if len(linha) == 4:
                        tipo, capacidade, descricao, ativa = linha
                        sala = {
                            "id": idx + 1,  # Adiciona um ID baseado na posição
                            "tipo": tipo,
                            "capacidade": capacidade,
                            "descricao": descricao,
                            "ativa": ativa
                        }
                        salas.append(sala)
                    else:
                        # Adicione um log ou mensagem de erro para linhas inválidas
                        print(f"Linha inválida encontrada no CSV: {linha}")
    return salas

# Função para adicionar uma nova sala ao arquivo CSV
def add_sala(sala):
    with open(salas_csv, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sala['tipo'], sala['capacidade'], sala['descricao'], sala['ativa']])

# Função para adicionar um novo usuário ao arquivo CSV
def add_usuario(usuario):
    with open(usuarios_csv, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([usuario['nome'], usuario['email'], usuario['password']])

# Função para verificar as credenciais do usuário
def verificar_usuario(email, password):
    if os.path.exists(usuarios_csv):
        with open(usuarios_csv, "r", newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for linha in reader:
                if linha:
                    _, email_arquivo, password_arquivo = linha
                    if email == email_arquivo and password == password_arquivo:
                        return True
    return False

# Função para adicionar uma reserva ao arquivo CSV
def add_reserva(reserva):
    with open(reservas_csv, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([reserva['sala'], reserva['inicio'], reserva['fim']])

# Função para ler reservas do arquivo CSV
def listar_reservas():
    reservas = []
    if os.path.exists(reservas_csv):
        with open(reservas_csv, "r", newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for linha in reader:
                if linha:  # Verifica se a linha não está vazia
                    sala, inicio, fim = linha
                    reserva = {"sala": sala, "inicio": inicio, "fim": fim}
                    reservas.append(reserva)
    return reservas

@app.route("/")
def home():
    return redirect("/cadastrar-sala")

@app.route("/cadastrar-sala", methods=["GET"])
def mostrar_formulario():
    return render_template("cadastrar-sala.html")

@app.route("/cadastrar-sala", methods=["POST"])
def cadastrar_sala():
    tipo = request.form["tipo"]
    capacidade = request.form["capacidade"]
    descricao = request.form["descricao"]
    sala = {"tipo": tipo, "capacidade": capacidade, "descricao": descricao, "ativa": "Ativa"}

    add_sala(sala)  # Adiciona a nova sala ao CSV
    
    return redirect("/listar-salas")

@app.route("/listar-salas")
def listar_salas_view():
    salas = ler_salas()  # Carrega salas cadastradas
    return render_template("listar-salas.html", salas=salas)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        password = request.form["password"]
        usuario = {"nome": nome, "email": email, "password": password}

        add_usuario(usuario)  # Adiciona o novo usuário ao CSV

        return redirect("/login")

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        if verificar_usuario(email, password):
            return redirect("/reservar-sala")  # Redireciona para a página de reservas após o login
        else:
            flash("E-mail ou senha inválidos")  # Exibe uma mensagem de erro
            
    return render_template("login.html")

@app.route("/reservar-sala", methods=["GET", "POST"])
def reservar_sala():
    if request.method == "POST":
        sala = request.form["sala"]
        inicio = request.form["inicio"]
        fim = request.form["fim"]
        
        reserva = {"sala": sala, "inicio": inicio, "fim": fim}
        
        add_reserva(reserva)  # Adiciona a nova reserva ao CSV
        
        return redirect("/reservas")  # Redireciona para a página de reservas

    return render_template("reservar-sala.html")

@app.route("/reservas")
def reservas():
    reservas = listar_reservas()  # Carrega reservas
    return render_template("reservas.html", reservas=reservas)

@app.route("/editar-sala/<int:id>", methods=["GET", "POST"])
def editar_sala(id):
    salas = ler_salas()
    if id < 1 or id > len(salas):
        flash("Sala não encontrada")
        return redirect("/listar-salas")

    sala = salas[id - 1]  # Assume que `id` começa em 1
    
    if request.method == "POST":
        tipo = request.form["tipo"]
        capacidade = request.form["capacidade"]
        descricao = request.form["descricao"]
        sala_atualizada = {"tipo": tipo, "capacidade": capacidade, "descricao": descricao, "ativa": sala["ativa"]}
        
        # Atualizar a sala no arquivo CSV
        with open(salas_csv, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["tipo", "capacidade", "descricao", "ativa"])
            for idx, s in enumerate(salas):
                if idx == id - 1:
                    writer.writerow([sala_atualizada['tipo'], sala_atualizada['capacidade'], sala_atualizada['descricao'], sala_atualizada['ativa']])
                else:
                    writer.writerow([s['tipo'], s['capacidade'], s['descricao'], s['ativa']])
        
        return redirect("/listar-salas")
    
    return render_template("login.html", sala=sala)

@app.route("/desativar-sala/<int:id>", methods=["POST"])
def desativar_sala(id):
    salas = ler_salas()
    if id < 1 or id > len(salas):
        flash("Sala não encontrada")
        return redirect("/listar-salas")

    sala = salas[id - 1]
    sala['ativa'] = "Inativa"

    # Atualizar o status da sala no arquivo CSV
    with open(salas_csv, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["tipo", "capacidade", "descricao", "ativa"])
        for idx, s in enumerate(salas):
            if idx == id - 1:
                writer.writerow([sala['tipo'], sala['capacidade'], sala['descricao'], sala['ativa']])
            else:
                writer.writerow([s['tipo'], s['capacidade'], s['descricao'], s['ativa']])
    
    return redirect("/listar-salas")

@app.route("/excluir-sala/<int:id>", methods=["POST"])
def excluir_sala(id):
    salas = ler_salas()
    if id < 1 or id > len(salas):
        flash("Sala não encontrada")
        return redirect("/listar-salas")

    salas = [sala for sala in salas if sala['id'] != id]  # Remove a sala com o ID fornecido
    
    # Reescrever o CSV sem a sala removida
    with open(salas_csv, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["tipo", "capacidade", "descricao", "ativa"])
        for sala in salas:
            writer.writerow([sala['tipo'], sala['capacidade'], sala['descricao'], sala['ativa']])
    
    return redirect("/listar-salas")

if __name__ == "__main__":
    app.run(debug=True)
