from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime

import time
from functools import wraps
import csv
import os

def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

def anonimizar_nome(nome):
    partes = nome.split()
    nome_anonimo = []
    for parte in partes:
        if len(parte) > 1:
            nome_anonimo.append(parte[0] + '*' * (len(parte) - 1))
        else:
            nome_anonimo.append(parte)
    return ' '.join(nome_anonimo)

def anonimizar_cpf(cpf):
    return cpf[:3] + '.***.***-**'

def anonimizar_email(email):
    if '@' in email:
        usuario, dominio = email.split('@')
        if len(usuario) > 1:
            return usuario[0] + '*' * (len(usuario) - 1) + '@' + dominio
    return email

def anonimizar_telefone(telefone):
    digitos = ''.join(filter(str.isdigit, telefone))
    return digitos[-4:]

@medir_tempo
def LGPD(row):
    id_, nome, cpf, email, telefone, data_nasc, created, updated = row
    return (
        id_,
        anonimizar_nome(nome),
        anonimizar_cpf(cpf),
        anonimizar_email(email),
        anonimizar_telefone(telefone),
        data_nasc,
        created,
        updated
    )

@medir_tempo
def gerar_arquivos_por_ano():
    if not os.path.exists('arquivos_gerados'):
        os.makedirs('arquivos_gerados')

    registros_por_ano = {}

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios;"))
        for row in result:
            row_anonimizada = LGPD(row)
            ano = row.data_nascimento.year
            if ano not in registros_por_ano:
                registros_por_ano[ano] = []
            registros_por_ano[ano].append(row_anonimizada)

    for ano, registros in registros_por_ano.items():
        nome_arquivo = f'arquivos_gerados/{ano}.csv'
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'created_on', 'updated_on'])
            writer.writerows(registros)

    print("Arquivos gerados:", list(registros_por_ano.keys()))

if __name__ == "__main__":
    gerar_arquivos_por_ano()