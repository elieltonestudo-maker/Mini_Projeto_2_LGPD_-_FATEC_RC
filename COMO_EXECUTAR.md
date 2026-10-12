# Como Baixar e Executar o Projeto

Este guia explica como baixar o projeto do GitHub e executa-lo no seu computador.

## Pre-requisitos

Antes de comecar, certifique-se de ter instalado:

- **Python 3.8 ou superior** - Download em https://www.python.org/downloads/
- **Git** - Download em https://git-scm.com/downloads

Para verificar se o Python esta instalado, abra o terminal e digite:

    python --version

Se aparecer algo como `Python 3.11.x`, esta tudo certo.

## Passo 1: Clonar o repositorio

Abra o terminal e navegue ate a pasta onde deseja salvar o projeto. Depois execute:

    git clone https://github.com/elieltonestudo-maker/Mini_Projeto_2_LGPD_-_FATEC_RC.git

Isso vai criar uma pasta chamada `Mini_Projeto_2_LGPD_-_FATEC_RC` com todos os arquivos do projeto.

Entre na pasta:

    cd Mini_Projeto_2_LGPD_-_FATEC_RC

## Passo 2: Criar e ativar o ambiente virtual

O ambiente virtual isola as dependencias do projeto, evitando conflitos com outras bibliotecas do sistema.

### No Windows:

    python -m venv venv
    venv\Scripts\activate

### No Linux ou Mac:

    python3 -m venv venv
    source venv/bin/activate

Apos ativar, o terminal vai mostrar `(venv)` no inicio da linha.

Se der erro de politica de execucao no Windows (PowerShell), execute:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Digite `S` (Sim) quando perguntar, e tente ativar novamente.

## Passo 3: Instalar as dependencias

Com o ambiente virtual ativo, execute:

    pip install -r requirements.txt

Isso vai instalar o SQLAlchemy, psycopg2-binary, Faker e outras dependencias.

Aguarde a conclusao. No final, deve aparecer `Successfully installed ...`.

## Passo 4: Executar o programa

Com o ambiente virtual ativo, execute:

    python LGPD.py

O programa vai exibir um menu interativo com as seguintes opcoes:

    ===== MINI PROJETO 2 - LGPD =====
    Este programa executa as atividades 2 e 3 do projeto.
    Atividade 2: gera arquivos CSV por ano com dados anonimizados.
    Atividade 3: gera todos.csv com nome e CPF originais.
    As atividades sao independentes. Escolha qualquer ordem.

    ===== MENU =====
    1 - Gerar arquivos por ano (Atividade 2)
    2 - Gerar arquivo todos.csv (Atividade 3)
    3 - Executar tudo
    4 - Comparar registros (original x anonimizado, 10 por vez)
    0 - Sair
    Escolha uma opcao:

Digite o numero da opcao desejada e pressione ENTER.

## Passo 5: Verificar os arquivos gerados

Apos executar as atividades, os seguintes arquivos serao criados:

- `arquivos_gerados/` - Pasta com um CSV para cada ano de nascimento (dados anonimizados).
- `todos.csv` - Arquivo com nome e CPF originais (sem anonimizacao).
- `execucao.log` - Arquivo de log com os tempos de execucao.

O programa exibe o caminho completo onde os arquivos foram salvos.

## Solucao de problemas

### Erro: "python nao e reconhecido"

O Python nao esta no PATH do sistema. Reinstale o Python marcando a opcao "Add Python to PATH" durante a instalacao.

### Erro: "git nao e reconhecido"

O Git nao esta instalado ou nao esta no PATH. Reinstale o Git.

### Erro: "PermissionError: [Errno 13] Permission denied"

Algum arquivo CSV esta aberto no Excel. Feche-o e tente novamente.

### Erro: "could not connect to server"

O banco de dados PostgreSQL nao esta acessivel. Verifique sua conexao com a internet ou se o servidor esta online.

### Erro: "ModuleNotFoundError"

As dependencias nao foram instaladas. Execute novamente:

    pip install -r requirements.txt

## Estrutura do projeto

    Mini_Projeto_2_LGPD_-_FATEC_RC/
    ├── LGPD.py                  # Codigo principal
    ├── requirements.txt         # Dependencias
    ├── todos.csv                # Gerado pela Atividade 3
    ├── execucao.log             # Log de execucao (Atividade 4)
    ├── Atividade_LGPD.pdf       # Enunciado do projeto
    ├── README.md                # Documentacao
    ├── COMO_EXECUTAR.md         # Este arquivo
    ├── arquivos_gerados/        # CSVs por ano (Atividade 2)
    └── venv/                    # Ambiente virtual

