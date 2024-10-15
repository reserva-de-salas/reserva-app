# Reserva App

Aplicação de exemplo para aulas sobre desenvolvimento web backend e criação de multipage applications utilizand Python e Flask.

## Usuários vs. Funcionalidades
- Administrador
  - Login
  - Reservar Sala
  - Ver Reservas
  - Cancelar Reserva
  - Gerenciar Salas
  - Logout
- Professor
  - Cadastrar
  - Login
  - Reservar Sala
  - Ver Reservas
  - Cancelar Reserva
  - Logout

## Models
- Usuário
  - codigo
  - nome
  - email
  - senha
  - ativo
  - admin
- Sala
  - codigo
  - capacidade
  - ativa
  - tipo
  - descricao
- Reserva
  - codigo
  - usuario
  - sala
  - data e hora início
  - data e hora fim
  - ativa
  
## Instalação e execução

1. Baixar e instalar o poetry
`curl -sSL https://install.python-poetry.org | python3 -`
`export PATH="$HOME/.local/bin:$PATH"`

- Nos laboratórios do IFSP
`export PATH="/home/estudante1/.local/bin:$PATH"`

2. Fazer o clone do repositório e abrir o projeto no VSCode
`git clone https://github.com/reserva-de-salas/reserva-app.git`

3. Ativar e instalar as dependências do ambiente virtual controlado pelo poetry no VSCode
`poetry shell`
`poetry install`

4. Instalar a extensão do python

5. Selecionar o interpretador python correto
`Ctrl + Shift + P`
Python: Select Interpreter

6. Executar o projeto
`poetry run flask --app diretorio_do_projeto/app.py run`

## Conexão com banco MySQL

1. Abrir o prompt de comando e ir até a pasta do projeto

2. Criação do ambiente virtual venv
`python -m venv venv`

- Nos laboratórios do IFSP
`python3 -m venv venv`

3. Ativar o ambiente virtual
`venv\Scripts\activate`

- Nos laboratórios do IFSP
`source venv/bin/activate`

4. Instalar o pacote do mysql-connector-python
`pip install mysql-connector-python`

5. Abrir o VSCode e ir até o diretório do projeto

6. Ativar o serviço do MySQL e criar uma banco de dados no MySQL Workbench

