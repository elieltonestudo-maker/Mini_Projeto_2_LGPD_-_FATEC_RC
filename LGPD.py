from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime

import time
from functools import wraps
import csv
import os
import logging

logging.basicConfig(
    filename='execucao.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        mensagem = f"Função '{func.__name__}' executada em {duracao:.6f} segundos."
        print(f"⏱ {mensagem}")
        logging.info(mensagem)
        return resultado
    return wrapper

class Anonimizador:
    def __init__(self, url_conexao):
        self.engine = create_engine(url_conexao, echo=False)
        self.metadata = MetaData()
        self.usuarios = Table(
            'usuarios', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('nome', String(50), nullable=False, index=True),
            Column('cpf', String(14), nullable=False),
            Column('email', String(100), nullable=False, unique=True),
            Column('telefone', String(20), nullable=False),
            Column('data_nascimento', Date, nullable=False),
            Column('created_on', DateTime(), default=datetime.now),
            Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
        )
        self.metadata.create_all(self.engine)

    def anonimizar_nome(self, nome):
        partes = nome.split()
        nome_anonimo = []
        for parte in partes:
            if len(parte) > 1:
                nome_anonimo.append(parte[0] + '*' * (len(parte) - 1))
            else:
                nome_anonimo.append(parte)
        return ' '.join(nome_anonimo)

    def anonimizar_cpf(self, cpf):
        return cpf[:3] + '.***.***-**'

    def anonimizar_email(self, email):
        if '@' in email:
            usuario, dominio = email.split('@')
            if len(usuario) > 1:
                return usuario[0] + '*' * (len(usuario) - 1) + '@' + dominio
        return email

    def anonimizar_telefone(self, telefone):
        digitos = ''.join(filter(str.isdigit, telefone))
        return digitos[-4:]

    @medir_tempo
    def anonimizar_registro(self, row):
        id_, nome, cpf, email, telefone, data_nasc, created, updated = row
        return (
            id_,
            self.anonimizar_nome(nome),
            self.anonimizar_cpf(cpf),
            self.anonimizar_email(email),
            self.anonimizar_telefone(telefone),
            data_nasc,
            created,
            updated
        )

    @medir_tempo
    def gerar_arquivos_por_ano(self):
        if not os.path.exists('arquivos_gerados'):
            os.makedirs('arquivos_gerados')

        registros_por_ano = {}

        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM usuarios;"))
            for row in result:
                row_anonimizada = self.anonimizar_registro(row)
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
        caminho = os.path.abspath('arquivos_gerados')
        print(f"Arquivos salvos em: {caminho}")

    @medir_tempo
    def gerar_arquivo_todos(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT nome, cpf FROM usuarios;"))
            with open('todos.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['nome', 'cpf'])
                for row in result:
                    writer.writerow([row.nome, row.cpf])
        print("Arquivo todos.csv gerado.")
        caminho = os.path.abspath('todos.csv')
        print(f"Arquivo salvo em: {caminho}")

    @medir_tempo
    def comparar_registros(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM usuarios;"))
            registros = []
            for row in result:
                original = tuple(row)
                anonimizado = self.anonimizar_registro(row)
                registros.append((original, anonimizado))

        total = len(registros)
        pagina = 10
        inicio = 0

        print(f"\nTotal de registros: {total}")
        print("Comparativo ORIGINAL x ANONIMIZADO (10 por vez).")
        print("Pressione ENTER para ver os proximos 10, ou 's' para sair.\n")

        while inicio < total:
            fim = min(inicio + pagina, total)
            for i in range(inicio, fim):
                original, anonimizado = registros[i]
                print(f"[{i + 1}] ORIGINAL:    {original}")
                print(f"    ANONIMIZADO: {anonimizado}")
                print()

            inicio = fim

            if inicio >= total:
                print("Fim dos registros.")
                break

            comando = input("ENTER para continuar, 's' para sair: ").strip().lower()
            if comando == 's':
                print("Exibicao interrompida.")
                break


if __name__ == "__main__":
    anonimizador = Anonimizador("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2")

    print("\n===== MINI PROJETO 2 - LGPD =====")
    print("Este programa executa as atividades 2 e 3 do projeto.")
    print("Atividade 2: gera arquivos CSV por ano com dados anonimizados.")
    print("Atividade 3: gera todos.csv com nome e CPF originais.")
    print("As atividades sao independentes. Escolha qualquer ordem.\n")

    while True:
        print("\n===== MENU =====")
        print("1 - Gerar arquivos por ano (Atividade 2)")
        print("2 - Gerar arquivo todos.csv (Atividade 3)")
        print("3 - Executar tudo")
        print("4 - Comparar registros (original x anonimizado, 10 por vez)")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            anonimizador.gerar_arquivos_por_ano()
        elif opcao == "2":
            anonimizador.gerar_arquivo_todos()
        elif opcao == "3":
            anonimizador.gerar_arquivos_por_ano()
            anonimizador.gerar_arquivo_todos()
        elif opcao == "4":
            anonimizador.comparar_registros()
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opcao invalida. Tente novamente.")