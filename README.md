# DataProcessorGCP

## Descrição

DataProcessorGCP é uma prova de conceito (POC) para uma aplicação que permite o upload de arquivos Excel e os processa para serem carregados em uma tabela no Google BigQuery. A aplicação é desenvolvida utilizando Python e Flask, e está atualmente em desenvolvimento.

## Estrutura do Projeto

├── app
│ ├── init.py
│ ├── config.py
│ ├── data_processor.py
│ ├── main
│ │ ├── init.py
│ │ ├── routes.py
│ │ └── templates
│ │ └── index.html
│ └── static
│ └── css
│ └── style.css
├── tests
│ ├── init.py
│ ├── test_data_processor.py
│ └── test_routes.py
├── uploads
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md


## Funcionalidades

- Carregamento de arquivos Excel
- Processamento dos dados do Excel
- Upload dos dados processados para o Google BigQuery

## Requisitos

- Python 3.10
- Flask
- pandas
- pandas_gbq
- google-auth
- python-dotenv

## Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/Gabriel-RdS/DataProcessorGCP.git
cd DataProcessorGCP
```
2. Crie um ambiente virtual e ative-o:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

3. Instale as dependências:

```bash
pip3 install -r requirements.txt
```

4. Configure suas variáveis de ambiente no arquivo .env:

```bash
FLASK_APP=run.py
FLASK_ENV=development
```

5. Execute a aplicação:

```bash
flask run
```

6. Acesse a aplicação em seu navegador em http://127.0.0.1:5000.

## Desenvolvimento

Este projeto está em desenvolvimento. As funcionalidades podem mudar e novas funcionalidades podem ser adicionadas.

## Contribuição

Se você deseja contribuir para este projeto, por favor, faça um fork do repositório, crie uma branch para suas funcionalidades ou correções, e envie um pull request.

