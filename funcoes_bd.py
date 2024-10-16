# Import da conexão
from datetime import datetime
from conexao_bd import conexao_fechar, conexao_abrir

# Todas as funções do banco precisam receber a conexão como parâmetro

def listarUsuarios(con):
     # O cursor é um objeto criado a partir da conexão que permite executar consultas SQL e interagir com os resultados
     # Ao criar um cursor com o argumento dictionary=True, será permitido que os resultados retornados pela consultam vão ser em formato de dicionário
     cursor = con.cursor(dictionary=True)
     # Comando SQL
     sql = "SELECT * FROM usuario"
     # Executar o sql
     cursor.execute(sql)
     # fetchall() retorna todas as linhas da tabela como dicionários em uma lista
     resultado = cursor.fetchall()
     # Fechar a conexão
     cursor.close()
     return resultado

def inserirUsuario(con, nome, email, salt, hash_senha):
     cursor = con.cursor()
     # Para consultas parametrizadas, deve-se usar %s para representar cada parâmetro
     sql = "INSERT INTO usuario (nome, email, salt, hash_senha) VALUES (%s, %s, %s, %s)"
     # Com consultas parametrizadas, o primeiro argumento do execute() deve ser o sql, 
     # já o segundo, os dados que serão passados como argumento no comando SQl em forma de tupla
     cursor.execute(sql, (nome, email, salt, hash_senha))
     # Confirmar as alterações feitas no banco
     con.commit() 
     cursor.close()


def inserirSala(con, tipo, capacidade, descricao, ativa):
     cursor = con.cursor()
     sql = "INSERT INTO salas (tipo, capacidade, descricao, ativa) VALUES (%s, %s, %s, %s)"
     cursor.execute(sql, (tipo, capacidade, descricao, ativa))
     con.commit() 
     cursor.close()

def listarSalas(con):
     cursor = con.cursor(dictionary=True)
     sql = "SELECT * FROM salas"
     cursor.execute(sql)
     resultado = cursor.fetchall()
     cursor.close()
     return resultado

def deletarSala(con, id):
     cursor = con.cursor()
     sql = "DELETE FROM salas WHERE id = %s"
     cursor.execute(sql, (id,))
     con.commit() 
     cursor.close()
        
def inserirReserva(con, id_sala, inicio, fim):
     cursor = con.cursor()
     sql = "INSERT INTO reservas (id_sala, inicio, fim) VALUES (%s, %s, %s)"
     cursor.execute(sql, (id_sala, inicio, fim))
     con.commit() 
     cursor.close()

def listarReservas(con):
     cursor = con.cursor(dictionary=True)
     sql = "SELECT * FROM reservas"
     cursor.execute(sql)
     resultado = cursor.fetchall()
     cursor.close()
     return resultado

def filtrarReservasPorSala(con, sala_id):
     cursor = con.cursor(dictionary=True)
     sql = "SELECT * FROM reservas WHERE id_sala = %s"
     cursor.execute(sql, (sala_id,))
     resultado = cursor.fetchall()
     cursor.close()
     return resultado

def filtrarReservasPorData(con, data):
     cursor = con.cursor(dictionary=True)

     data_type_datetime = datetime.strptime(data, "%Y-%m-%d")

     data_inicio = data_type_datetime.strftime("%Y-%m-%d 00:00:00")  # Início do dia
     data_fim = data_type_datetime.strftime("%Y-%m-%d 23:59:59")

     sql = "SELECT * FROM reservas WHERE (inicio BETWEEN %s AND %s) OR (fim BETWEEN %s AND %s) OR (inicio < %s AND fim > %s)"
     cursor.execute(sql, (data_inicio, data_fim, data_inicio, data_fim, data_inicio, data_fim))
     resultado = cursor.fetchall()
     cursor.close()
     return resultado

def filtrarReservasPorDataESala(con, data, sala_id):
     cursor = con.cursor(dictionary=True)

     data_type_datetime = datetime.strptime(data, "%Y-%m-%d")

     data_inicio = data_type_datetime.strftime("%Y-%m-%d 00:00:00")  # Início do dia
     data_fim = data_type_datetime.strftime("%Y-%m-%d 23:59:59")

     sql = "SELECT * FROM reservas WHERE ((inicio BETWEEN %s AND %s) OR (fim BETWEEN %s AND %s) OR (inicio < %s AND fim > %s)) AND id_sala = %s"
     cursor.execute(sql, (data_inicio, data_fim, data_inicio, data_fim, data_inicio, data_fim, sala_id))
     resultado = cursor.fetchall()
     cursor.close()
     return resultado

def deletarReserva(con, id):
     cursor = con.cursor()
     sql = "DELETE FROM reservas WHERE id = %s"
     cursor.execute(sql, (id,))
     con.commit() 
     cursor.close()

def criarBanco(con):
     with open("banco.sql", "r") as file:
          sql = file.read()

     cursor = con.cursor()
     cursor.execute(sql)
     cursor.close()

def alterarAtivaSala(con, id):
     cursor = con.cursor()
     sql = "UPDATE salas SET ativa = NOT ativa WHERE id = %s"
     cursor.execute(sql, (id,))
     con.commit() 
     cursor.close()

def obterSalaPorId(con, id):
     cursor = con.cursor(dictionary=True)
     sql = "SELECT * FROM salas WHERE id = %s"
     cursor.execute(sql, (id,))
     resultado = cursor.fetchone()
     cursor.close()
     return resultado

def editarSala(con, id, tipo, capacidade, descricao):
     cursor = con.cursor(dictionary=True)
     sql = "UPDATE salas SET tipo = %s, capacidade = %s, descricao = %s WHERE id = %s"
     cursor.execute(sql, (tipo, capacidade, descricao, id))
     con.commit() 
     cursor.close()

# Fazer consulta com filtro pra reserva e UPDATE em salas

# Conexão 
# con = conexao_abrir("localhost", "estudante1", "estudante1", "teste_python")    