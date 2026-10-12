# Mini Projeto 2 - LGPD - FATEC Rio Claro

Segundo Mini Projeto da disciplina de Linguagem de Programacao II na FATEC Rio Claro, abordando a Lei Geral de Protecao de Dados (LGPD).

**Aluno:** Elielton Barbosa
**Professor:** Orlando Saraiva Junior
**Disciplina:** Linguagem de Programacao II
**Instituicao:** FATEC Rio Claro

## Sobre o Projeto

Este projeto implementa tecnicas de anonimizacao de dados pessoais em conformidade com a LGPD. O sistema le registros de usuarios de um banco de dados PostgreSQL, aplica regras de anonimizacao nos campos sensiveis (nome, CPF, e-mail e telefone) e gera arquivos CSV organizados por ano de nascimento.

## Atividades Implementadas

### Atividade 1 - Anonimizacao de Dados

- **Nome:** mantem a primeira letra de cada palavra e substitui o restante por asteriscos.
  - Exemplo: `Agatha Alves` -> `A***** A****`
- **CPF:** mantem os 3 primeiros digitos e mascara o restante.
  - Exemplo: `630.512.784-08` -> `630.***.***-**`
- **E-mail:** mantem a primeira letra do usuario e o dominio completo.
  - Exemplo: `tgarcia@example.com` -> `t******@example.com`
- **Telefone:** mantem apenas os 4 ultimos digitos.
  - Exemplo: `+55 71 6517-0929` -> `0929`

### Atividade 2 - Arquivos por Ano

Gera um arquivo CSV para cada ano de nascimento presente no banco de dados, contendo os registros anonimizados. Os arquivos sao salvos na pasta `arquivos_gerados/`.

### Atividade 3 - Arquivo Unico `todos.csv`

Gera um arquivo `todos.csv` na raiz do projeto contendo apenas os campos nome e CPF, sem anonimizacao.

### Atividade 4 - Logs no Decorador

Adapta o decorador `medir_tempo` para gravar o tempo de execucao das funcoes em um arquivo de log (`execucao.log`), alem de exibir no terminal.

## Extras Implementados

- **Refatoracao para Classe:** O codigo foi refatorado para usar a classe `Anonimizador`, agrupando os metodos de anonimizacao e geracao de arquivos.
- **Menu Interativo:** O usuario pode escolher qual atividade executar atraves de um menu no terminal.
- **Comparativo:** Opcao para comparar registros originais e anonimizados lado a lado, 10 por vez.
- **Caminhos dos Arquivos:** Exibe o caminho absoluto onde os arquivos foram salvos.

## Tecnologias Utilizadas

- Python 3
- SQLAlchemy (conexao com o banco de dados)
- PostgreSQL (banco de dados)
- Bibliotecas padrao: `csv`, `os`, `logging`, `time`, `functools`

## Como Executar

As instrucoes detalhadas de instalacao e execucao estao no arquivo [COMO_EXECUTAR.md](COMO_EXECUTAR.md).

Resumo rapido:

    git clone https://github.com/elieltonestudo-maker/Mini_Projeto_2_LGPD_-_FATEC_RC.git
    cd Mini_Projeto_2_LGPD_-_FATEC_RC
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python LGPD.py

## Estrutura do Projeto

    Mini_Projeto_2_LGPD_-_FATEC_RC/
    ├── LGPD.py                  # Codigo principal
    ├── requirements.txt         # Dependencias
    ├── todos.csv                # Gerado pela Atividade 3
    ├── execucao.log             # Log de execucao (Atividade 4)
    ├── Atividade_LGPD.pdf       # Enunciado do projeto
    ├── README.md                # Documentacao
    ├── COMO_EXECUTAR.md         # Guia de execucao
    ├── arquivos_gerados/        # CSVs por ano (Atividade 2)
    └── venv/                    # Ambiente virtual

## Observacoes

- O arquivo `todos.csv` contem dados reais (nao anonimizados), conforme solicitado na Atividade 3.
- Os arquivos da pasta `arquivos_gerados/` sao gerados dinamicamente e nao sao versionados no Git.
- O log `execucao.log` e sobrescrito a cada execucao.