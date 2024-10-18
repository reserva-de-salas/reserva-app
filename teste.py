import bisect
import csv
import hashlib
import os
import re
import secrets
from flask import Flask, flash, render_template, redirect, request, session
from datetime import datetime, timedelta
from funcoes_bd import *
from conexao_bd import conexao_abrir, conexao_fechar

app = Flask(__name__, template_folder="../templates")
app.secret_key = 'sua_chave_secreta'  # Necessário para usar a funcionalidade de mensagens
 
con_params = ("localhost", "troarmen", "0000", "reservasalas")   

con = conexao_abrir(*con_params)
criarBanco(con)
inserirSala(con, "quimica", 1, "descri", True)
conexao_fechar(con)