# Import da conexão
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


def inserirSala(con, tipo, descricao, capacidade, ativa):
     cursor = con.cursor()
     sql = "INSERT INTO salas (tipo, descricao, capacidade, ativa) VALUES (%s, %s, %s, %s)"
     cursor.execute(sql, (tipo, descricao, capacidade, ativa))
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
     cursor.execute(sql, (id))
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

     
def deletarReserva(con, id):
     cursor = con.cursor()
     sql = "DELETE FROM reservas WHERE id = %s"
     cursor.execute(sql, (id))
     con.commit() 
     cursor.close()

def criarBanco(con):
     with open("banco.sql", "r") as file:
          sql = file.read()

     cursor = con.cursor()
     cursor.execute(sql)
     cursor.close()
     
# Fazer consulta com filtro pra reserva e UPDATE em salas

# Conexão 
# con = conexao_abrir("localhost", "estudante1", "estudante1", "teste_python")    