# Import do módulo necessario para se concetar ao banco mysql com python
import mysql.connector;
import mariadb

# Função para abrir uma conexão com o banco
    # host = O endereço do servidor de banco de dados MySQL (localhost caso esteja na mesma máquina)
    # usuario = Nome do usuário do banco de dados MySQL
    # senha = Senha do usuário
    # banco = Nome do banco de dados
# Retorna a instância da conexão que pode ser usada para executar consultas SQL e outras operações no banco de dados
def conexao_abrir(host, usuario, senha, banco):
    #return mysql.connector.connect(host=host, user=usuario, password=senha, database=banco)
    try:
        print("Deu certo!")
        return mariadb.connect(host=host, user=usuario, password=senha, database=banco)
    except mariadb.Error as e:
        print(f"Erro ao conectar: {e}")
        return None

# Função para fechar a conexão com o banco
def conexao_fechar(con):
    con.close
