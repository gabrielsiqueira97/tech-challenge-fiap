import sqlite3

def get_db_connection():
    conn = sqlite3.connect("C:\\Users\\Gabriel\\Desktop\\FIAP\\Tech Challeng FIAP\\projeto_api_embrapa\\data\\database.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()
cursor = conn.cursor()

# Criar tabela
def criar_tabela_processamento_uvas():
    cursor.execute("DROP TABLE IF EXISTS processamento_uvas") 
    cursor.execute("""
    CREATE TABLE processamento_uvas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_de_uva TEXT NOT NULL,      
        grupo_de_uva TEXT NOT NULL,
        nm_uva TEXT NOT NULL,
        ano INTEGER NOT NULL,
        quantidade_kg INTEGER
    );
    """)
    conn.commit()
    conn.close()
    print("Tabela processamento uvas criada!")

def criar_tabela_producao_produtos():
    cursor.execute("DROP TABLE IF EXISTS producao_produtos") 
    cursor.execute("""
    CREATE TABLE producao_produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_principal TEXT NOT NULL,
        subproduto TEXT NOT NULL,
        quantidade INTEGER,
        ano INTEGER NOT NULL
    );
    """)
    conn.commit()
    conn.close()
    print("Tabela produção produtos criada!")

def criar_tabela_comercializacao_produtos():
    cursor.execute("DROP TABLE IF EXISTS comercializacao_produtos")  # Garante que a tabela seja recriada
    cursor.execute("""
    CREATE TABLE comercializacao_produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_principal TEXT NOT NULL,
        subproduto TEXT NOT NULL,
        quantidade_l INTEGER,
        ano INTEGER NOT NULL
    );
    """)

    conn.commit()
    print("Tabela comercialização produtos criada!")

def criar_tabela_importacao_produtos():
    cursor.execute("DROP TABLE IF EXISTS importacao_produtos")  # Garante que a tabela seja recriada
    cursor.execute("""
    CREATE TABLE importacao_produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pais TEXT NOT NULL,
        quantidade_kg INTEGER,
        valor_usd REAL,
        tipo_de_uva TEXT,
        ano INTEGER NOT NULL                   
    );
    """)
    conn.commit()
    print("Tabela importação de produtos criada!")


def criar_tabela_exportacao_produtos():
    cursor.execute("DROP TABLE IF EXISTS exportacao_produtos")  # Garante que a tabela seja recriada
    cursor.execute("""
    CREATE TABLE exportacao_produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pais TEXT NOT NULL,
        quantidade_kg INTEGER,
        valor_usd REAL,
        tipo_de_uva TEXT,
        ano INTEGER NOT NULL                   
    );
    """)
    conn.commit()
    print("Tabela exportação de produtos criada!")

def criar_tabela_usuarios():
    """Cria a tabela de usuários no banco de dados"""
    cursor.execute("DROP TABLE IF EXISTS usuarios") 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_usuario TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL
    );
    """)
    
    conn.commit()
    conn.close()
    print("Tabela usuarios criada!")


criar_tabela_processamento_uvas()
criar_tabela_producao_produtos()
criar_tabela_comercializacao_produtos()
criar_tabela_importacao_produtos()
criar_tabela_exportacao_produtos()
criar_tabela_usuarios()