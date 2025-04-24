
# Projeto API Embrapa

Este projeto realiza o **web scraping de dados da Embrapa**, armazena as informações localmente em um banco de dados **SQLite3** e disponibiliza os dados via uma **API REST criada com FastAPI**, protegida por autenticação **JWT**.

## Principais Tecnologias Utilizadas

- Python 3.10+
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - para Web Scraping
- [SQLite3](https://www.sqlite.org/index.html) - banco de dados local
- [FastAPI](https://fastapi.tiangolo.com/) - para construção da API
- JWT (JSON Web Tokens) - para autenticação
- [pytest](https://docs.pytest.org/) - para testes

Sugiro que entre no requirements.txt para ver todas as dependencias
---

## 📁 Estrutura do Projeto

```
projeto_api_embrapa/
│
├── app/                      # Código principal da aplicação FastAPI
│   ├── __init__.py
│   ├── routes.py             # Definições de rotas da API
│   ├── models.py             # Tem as classes do projeto
│   ├── services.py           # Lógica de negócio
│   ├── auth.py               # Autenticação JWT
│
├── config/
│   └── settings.py           # Configurações globais (.env, caminhos, etc.)
│
├── docs/
│   ├── README.md             # Este arquivo
│   └── api_documentation.md # Documentação detalhada da API (endpoints, exemplos, etc.)
│
├── tests/
│   └── test_routes.py        # Testes automatizados
│
├── data/
│   └── database.db           # Banco de dados SQLite
│
├── scripts/
│   ├── ws_processamento.py   # Script de web scraping - processamento
│   ├── ws_producao.py        # Script de web scraping - produção
│   └── db_tables.py          # Criação de tabelas do banco de dados
│
├── .env                      # Variáveis de ambiente (credenciais, segredos)
├── main.py                   # Arquivo principal para execução da API
├── requirements.txt          # Dependências do projeto
```

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/
cd projeto_api_embrapa
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```


### 4. Execute os scripts de scraping e banco
```bash
python scripts/db_tables.py
python scripts/ws_processamento.py
python scripts/ws_producao.py
```

### 5. Rode a aplicação FastAPI
```bash
uvicorn main:app --reload
```

A API estará disponível em: http://127.0.0.1:8000  
A documentação interativa pode ser acessada via: http://127.0.0.1:8000/docs

---

## 🔐 Autenticação JWT

Para acessar os endpoints protegidos:
1. Crie seu usuário e senha no `/cadastro_usuario`
2. Faça login via `/login` com usuário e senha definidos (via banco), para receber o TOKEN JWT.
3. Utilize o token retornado no campo TOKEN das chamadas GET protegidas.


---

## 🧪 Testes - EM DEV

Para rodar os testes automatizados:
```bash
pytest tests/
```
---

## 📌 Contribuição

Contribuições são bem-vindas! Fique à vontade para abrir **issues**, propor melhorias ou enviar um **pull request**.

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](../LICENSE).
