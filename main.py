from conexao_bd import conexao_fechar, conexao_abrir

# def clienteListar(con):
#     cursor = con.cursor()
#     sql = "SELECT * FROM cliente"
#     # Criando o cursor com a opção de retorno como dicionário   
#     cursor = con.cursor(dictionary=True)
#     cursor.execute(sql)
# # 
#     for (registro) in cursor:
#         print(registro['cli_nome'] + " - "+ registro['cli_fone'])

#     cursor.close()
#     #con.commit()    #mesma coisa q editar e não salvar


def inserirUsuario(con, nome, email, salt, hash_senha):
     cursor = con.cursor()
     sql = "INSERT INTO usuario (nome, email, salt, hash_senha) VALUES (%s, %s, %s, %s)"
     cursor.execute(sql, (nome, email, salt, hash_senha))
     con.commit() 
     cursor.close()

def listarUsuarios(con):
     cursor = con.cursor()
     sql = "SELECT * FROM usuario"
     cursor = con.cursor(dictionary=True)
     cursor.execute(sql)
     con.commit() 
     cursor.close()

def inserirSala(con, tipo, descricao, capacidade, ativa):
     cursor = con.cursor()
     sql = "INSERT INTO salas (tipo, descricao, capacidade, ativa) VALUES (%s, %s, %s, %s)"
     cursor.execute(sql, (tipo, descricao, capacidade, ativa))
     con.commit() 
     cursor.close()

def listarSalas(con):
     cursor = con.cursor()
     sql = "SELECT * FROM salas"
     cursor = con.cursor(dictionary=True)
     cursor.execute(sql)
     con.commit() 
     cursor.close()

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
     cursor = con.cursor()
     sql = "SELECT * FROM reservas"
     cursor = con.cursor(dictionary=True)
     cursor.execute(sql)
     con.commit() 
     cursor.close()

     
def deletarReserva(con, id):
     cursor = con.cursor()
     sql = "DELETE FROM reservas WHERE id = %s"
     cursor.execute(sql, (id))
     con.commit() 
     cursor.close()

# Fazer consulta com filtro pra reserva e UPDATE em salas


# def main():
#     con = conexao_abrir("localhost", "estudante1", "estudante1", "teste_python")
    
#     clienteListar(con)

#     conexao_fechar(con)




# if __name__ == "__main__":
# 	main()