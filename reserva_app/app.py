import csv
import os
import re
from flask import Flask, flash, render_template, redirect, request
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
criar_arquivo_csv(usuarios_csv, ["nome", "email", "senha"])
criar_arquivo_csv(reservas_csv, ["sala", "inicio", "fim"])

def listar_salas():
    salas = []
    with open(salas_csv, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for linha in reader:
            salas.append(linha)
    return salas

def procurar_proximo_id():
    ids = []
    with open(salas_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for linha in reader:
            if linha['id'].isdigit():
                ids.append(int(linha['id']))
    return max(ids) + 1 if ids else 1

def add_sala(sala):
    sala['id'] = procurar_proximo_id()
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

def add_usuario(usuario):
    if verificar_usuario(usuario['email'], usuario['senha'], True):
        with open(usuarios_csv, "a", encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([usuario['nome'], usuario['email'], usuario['senha']])
        return True
    return False

def verificar_login(email, senha):
    with open(usuarios_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if len(linha) == 3 and linha[1] == email and linha[2] == senha:
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
    with open(reservas_csv, "a", encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([reserva['sala'], reserva['inicio'], reserva['fim']])

def listar_reservas():
    reservas = []
    with open(reservas_csv, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for linha in reader:
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
    return redirect("/reservas")

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
        return redirect('cadastrar-sala')
    
    capacidade = int(capacidade)

    if capacidade < 10 or capacidade > 150:
        flash("As salas de aula devem ter capacidade para comportar entre 10 e 150 alunos.")
        return redirect('cadastrar-sala')   


    if len(descricao) > 150:
        flash("A descrição de uma sala pode ter até 150 caracteres.")  
        return redirect('cadastrar-sala')   

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
            return redirect('cadastro')
        
        usuario = {"nome": nome, "email": email, "senha": senha}

        if not verificar_existencia_de_usuario(email) or not add_usuario(usuario):
            return redirect("/cadastro")

        return redirect("/reservas")

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if  not email or not senha:
            flash("Preencha todos os campos.")
            return redirect('login')
        
        if verificar_usuario(email, senha, False):
            if verificar_login(email, senha):
                return redirect("/reservas")  
            
        flash("E-mail e/ou senha inválidos")
            
    return render_template("login.html")

@app.route("/reservar-sala", methods=["GET", "POST"])
def reservar_sala():
    if request.method == "POST":
        sala = request.form("sala")
        inicio = request.form("inicio")
        fim = request.form("fim")

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

    if not sala:
        flash("Sala não encontrada")
        return redirect("/listar-salas")

    if request.method == "POST":
        tipo = request.form["tipo"]
        capacidade = request.form["capacidade"]
        descricao = request.form["descricao"]

        if not tipo or not capacidade:
            flash("Preencha os campos de tipo e capacidade.")
            return redirect(f'/editar-sala/{id}')
        
        try:
            capacidade = int(capacidade)
        except ValueError:
            flash("Capacidade deve ser um número válido.")
            return redirect(f'/editar-sala/{id}')

        if capacidade < 10 or capacidade > 150:
            flash("As salas de aula devem ter capacidade para comportar entre 10 e 150 alunos.")
            return redirect(f'/editar-sala/{id}')   

        if len(descricao) > 150:
            flash("A descrição de uma sala pode ter até 150 caracteres.")  
            return redirect(f'/editar-sala/{id}')   

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
    if id < 1 or id > len(salas):
        flash("Sala não encontrada")
        return redirect("/listar-salas")

    sala = salas[id - 1]
    
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
    if id < 1 or id > len(salas):
        flash("Sala não encontrada")
        return redirect("/listar-salas")

    salas = [sala for sala in salas if int(sala['id']) != id]

    with open(salas_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "tipo", "descricao", "capacidade", "ativa"])
        writer.writeheader()
        for sala in salas:
            writer.writerow(sala)
    
    return redirect("/listar-salas")

if __name__ == "__main__":
    app.run(debug=True)
