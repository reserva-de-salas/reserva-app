import csv
import hashlib
import os
import re
import secrets
from flask import Flask, flash, render_template, redirect, request, session
from datetime import datetime, timedelta


app = Flask(__name__, template_folder="../templates")
app.secret_key = 'sua_chave_secreta'  # Necessário para usar a funcionalidade de mensagens

salas_csv = "salas.csv"
usuarios_csv = "usuarios.csv"
reservas_csv = "reservas.csv"

def criar_arquivo_csv(file_path, headers):
    if not os.path.exists(file_path):
        with open(file_path, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

criar_arquivo_csv(salas_csv, ["id", "tipo", "descricao", "capacidade", "ativa"])
criar_arquivo_csv(usuarios_csv, ["nome", "email", "salt", "hash_senha"])
criar_arquivo_csv(reservas_csv, ["id", "sala", "inicio", "fim"])

def listar_salas():
    salas = []
    with open(salas_csv, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for linha in reader:
            salas.append(linha)
    return salas

def procurar_proximo_id(arquivo_csv):
    ids = []
    with open(arquivo_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for linha in reader:
            if linha['id'].isdigit():
                ids.append(int(linha['id']))
    return max(ids) + 1 if ids else 1

def add_sala(sala):
    sala['id'] = procurar_proximo_id(salas_csv)
    with open(salas_csv, "a", encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "tipo", "descricao", "capacidade", "ativa"])
        writer.writerow(sala)

def validar_email(email, c):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(padrao, email):
        if c:
            flash("Email inválido.")
        return False
    return True

def validar_senha(senha, c):
    padrao = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
    if not re.match(padrao, senha):
        if c:
            flash("A senha deve possuir pelo menos 8 caracteres, uma letra maiúscula, uma letra minúscula e um número.")
        return False
    return True

def verificar_usuario(email, senha, c):
    if not validar_email(email, c) or not validar_senha(senha, c):
        return False
    return True

def hash_senha_com_salt(senha):
    salt = secrets.token_hex(16)
    hash_senha = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return salt, hash_senha

def add_usuario(usuario):
    if verificar_usuario(usuario['email'], usuario['senha'], True):
        salt, hash_senha = hash_senha_com_salt(usuario['senha'])

        with open(usuarios_csv, "a", encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([usuario['nome'], usuario['email'], salt, hash_senha])

        return True
    
    return False

def hash_senha(senha, salt):
    return hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

def verificar_login(email, senha):
    with open(usuarios_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for linha in reader:
            if len(linha) == 4 and linha[1] == email:
                salt_armazenado = linha[2]
                hashed_senha_armazenada = linha[3]

                hashed_senha = hash_senha(senha, salt_armazenado)

                if hashed_senha == hashed_senha_armazenada:
                    return True
    return False

def verificar_existencia_de_usuario(email):
    with open(usuarios_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if len(linha) == 3 and linha[1] == email:
                flash("Já existe uma conta com esse E-mail.")
                return False
    return True

def add_reserva(reserva):
    reserva['id'] = procurar_proximo_id(reservas_csv)
    with open(reservas_csv, "a", encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([reserva['id'], reserva['sala'], reserva['inicio'], reserva['fim']])

def listar_reservas():
    reservas = []
    agora = datetime.now()

    with open(reservas_csv, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for linha in reader:
            fim_str = linha.get("fim")
            fim = datetime.fromisoformat(fim_str)
            
            if fim > agora:
                reservas.append(linha)
            
    return reservas

def validar_duracao_reserva(inicio_str, fim_str):
        inicio = datetime.fromisoformat(inicio_str)
        fim = datetime.fromisoformat(fim_str)
        duracao = fim - inicio
        min_duracao = timedelta(minutes=45)
        max_duracao = timedelta(minutes=180)

        return min_duracao <= duracao <= max_duracao
            

def reservas_conflitam(nova_reserva, reservas_existentes):
    inicio_nova = datetime.fromisoformat(nova_reserva['inicio'])
    fim_nova = datetime.fromisoformat(nova_reserva['fim'])
    sala_nova = nova_reserva['sala']
    
    for reserva in reservas_existentes:
        inicio_existente = datetime.fromisoformat(reserva['inicio'])
        fim_existente = datetime.fromisoformat(reserva['fim'])
        sala_existente = reserva['sala']
        
        if sala_nova == sala_existente and (inicio_nova < fim_existente) and (fim_nova > inicio_existente):
            return reserva
        
    return None

def validar_antecedencia_reserva(inicio_str):
    inicio = datetime.fromisoformat(inicio_str)
    agora = datetime.now()
    antecedencia_minima = timedelta(days=1)
    antecedencia_maxima = timedelta(days=30)

    return inicio >= agora + antecedencia_minima and inicio <= agora + antecedencia_maxima

@app.route("/")
def home():
    if 'email' in session:
        return redirect("/reservas")
    return redirect("/login")

@app.route("/cadastrar-sala", methods=["GET"])
def mostrar_formulario():
    return render_template("cadastrar-sala.html")

@app.route("/cadastrar-sala", methods=["POST"])
def cadastrar_sala():
    tipo = request.form["tipo"]
    capacidade = request.form["capacidade"]
    descricao = request.form["descricao"]

    if not tipo or not capacidade:
        flash("Preencha os campos de tipo e capacidade.")
        return render_template('cadastrar-sala.html', tipo=tipo, capacidade=capacidade, descricao=descricao)
    
    capacidade = int(capacidade)

    if capacidade < 10 or capacidade > 150:
        flash("As salas de aula devem ter capacidade para comportar entre 10 e 150 alunos.")
        return render_template('cadastrar-sala.html', tipo=tipo, capacidade=capacidade, descricao=descricao)


    if len(descricao) > 150:
        flash("A descrição de uma sala pode ter até 150 caracteres.")  
        return render_template('cadastrar-sala.html', tipo=tipo, capacidade=capacidade, descricao=descricao)

    sala = {"tipo": tipo, "capacidade": capacidade, "descricao": descricao, "ativa": "Ativa"}

    add_sala(sala)  
    
    return redirect("/listar-salas")

@app.route("/listar-salas")
def listar_salas_view():
    salas = listar_salas()
    return render_template("listar-salas.html", salas=salas)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if not nome or not email or not senha:
            flash("Preencha todos os campos.")
            return render_template('cadastro.html', nome=nome, email=email, senha=senha)
        
        usuario = {"nome": nome, "email": email, "senha": senha}

        if not verificar_existencia_de_usuario(email) or not add_usuario(usuario):
            return render_template('cadastro.html', nome=nome, email=email, senha=senha)

        return redirect("/reservas")

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if  not email or not senha:
            flash("Preencha todos os campos.")
            return render_template('login.html', email=email, senha=senha)
        
        if verificar_usuario(email, senha, False):
            if verificar_login(email, senha):
                return redirect("/reservas")  
            
        flash("E-mail e/ou senha inválidos")
        return render_template('login.html', email=email, senha=senha)
            
    return render_template("login.html")

@app.route("/reservar-sala", methods=["GET", "POST"])
def reservar_sala():
    if request.method == "POST":
        sala = request.form.get("sala")
        inicio = request.form.get("inicio")
        fim = request.form.get("fim")

        if not sala or not inicio or not fim:
            flash("Preencha todos os campos.")
            return render_template('reservar-sala.html', sala=sala, inicio=inicio, fim=fim, salas=listar_salas())

        if not validar_duracao_reserva(inicio, fim):
            flash("Uma reserva deve ter entre 45 e 180 minutos.")
            return render_template('reservar-sala.html', sala=sala, inicio=inicio, fim=fim, salas=listar_salas())

        if not validar_antecedencia_reserva(inicio):
            flash("Uma sala deve ser reservada com no mínimo um dia e no máximo 30 dias de antecedência.")
            return render_template('reservar-sala.html', sala=sala, inicio=inicio, fim=fim, salas=listar_salas())
        
        reserva = {"sala": sala, "inicio": inicio, "fim": fim}
        reserva_conflitante = reservas_conflitam(reserva, listar_reservas())
    
        if reserva_conflitante:
            flash(f"Já há uma reserva para esta sala em {datetime.fromisoformat(reserva_conflitante['inicio']).strftime('%d/%m/%Y %H:%M')} até {datetime.fromisoformat(reserva_conflitante['fim']).strftime('%d/%m/%Y %H:%M')}.")
            return render_template('reservar-sala.html', sala=sala, inicio=inicio, fim=fim, salas=listar_salas())
        
        add_reserva(reserva) 
        
        return redirect("/reservas")  

    salas = listar_salas()  
    return render_template("reservar-sala.html", salas=salas)

@app.route("/reservas")
def reservas():
    reservas = listar_reservas() 
    return render_template("reservas.html", reservas=reservas)

@app.route("/editar-sala/<int:id>", methods=["GET", "POST"])
def editar_sala(id):
    salas = listar_salas()
    sala = next((s for s in salas if int(s['id']) == id), None)

    if request.method == "POST":
        tipo = request.form["tipo"]
        capacidade = request.form["capacidade"]
        descricao = request.form["descricao"]

        if not tipo or not capacidade:
            flash("Preencha os campos de tipo e capacidade.")
            return render_template("cadastrar-sala.html", sala={
                "id": id,
                "tipo": tipo,
                "capacidade": capacidade,
                "descricao": descricao,
                "ativa": sala["ativa"]
            })
        
        capacidade = int(capacidade)

        if capacidade < 10 or capacidade > 150:
            flash("As salas de aula devem ter capacidade para comportar entre 10 e 150 alunos.")
            return render_template("cadastrar-sala.html", sala={
                "id": id,
                "tipo": tipo,
                "capacidade": capacidade,
                "descricao": descricao,
                "ativa": sala["ativa"]
            })

        if len(descricao) > 150:
            flash("A descrição de uma sala pode ter até 150 caracteres.")
            return render_template("cadastrar-sala.html", sala={
                "id": id,
                "tipo": tipo,
                "capacidade": capacidade,
                "descricao": descricao,
                "ativa": sala["ativa"]
            })

        sala_atualizada = {
            "id": id,
            "tipo": tipo,
            "capacidade": capacidade,
            "descricao": descricao,
            "ativa": sala["ativa"]
        }

        salas = [sala_atualizada if int(s['id']) == id else s for s in salas]

        with open(salas_csv, "w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "tipo", "descricao", "capacidade", "ativa"])
            writer.writeheader()
            writer.writerows(salas)

        return redirect("/listar-salas")

    return render_template("cadastrar-sala.html", sala=sala)

@app.route("/alterar-status-sala/<int:id>", methods=["POST"])
def alterar_status_sala(id):
    salas = listar_salas()

    for s in salas:
        if int(s['id']) == id:
            sala = s
    
    if sala['ativa'] == "Ativa":
        sala['ativa'] = "Inativa"
    else:
        sala['ativa'] = "Ativa"

    with open(salas_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "tipo", "descricao", "capacidade", "ativa"])
        writer.writeheader()
        for s in salas:
            writer.writerow(s)
    
    return redirect("/listar-salas")

@app.route("/excluir-sala/<int:id>", methods=["POST"])
def excluir_sala(id):
    salas = listar_salas()

    salas = [sala for sala in salas if int(sala['id']) != id]

    with open(salas_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "tipo", "descricao", "capacidade", "ativa"])
        writer.writeheader()
        for sala in salas:
            writer.writerow(sala)
    
    return redirect("/listar-salas")

@app.route("/excluir-reserva/<int:id>", methods=["POST"])
def excluir_reserva(id):
    reservas = listar_reservas()

    reservas = [reserva for reserva in reservas if int(reserva['id']) != id]

    with open(reservas_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "sala", "inicio", "fim"])
        writer.writeheader()
        for reserva in reservas:
            writer.writerow(reserva)
    
    return redirect("/reservas")

if __name__ == "__main__":
    app.run(debug=True)
