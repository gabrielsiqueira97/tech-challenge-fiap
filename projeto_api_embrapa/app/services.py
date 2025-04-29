import sqlite3
from app.models import ProducaoUva
from app.models import ProcessamentoUva
from app.models import ComercializacaoProduto, ExportacaoProduto, ImportacaoProduto


def get_db_connection():
    """Conectar ao banco SQLite"""
    conn = sqlite3.connect("data/database.db")
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    return conn

def consultar_producao_por_ano(ano: int):
    """Consulta produtos de um determinado ano no banco"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM producao_produtos WHERE ano = ?", (ano,))
    dados = cursor.fetchall()
    
    conn.close()
    
    return [ProducaoUva(**dict(row)) for row in dados]  # Retorna lista de objetos Pydantic

#Funções para pagina(GET) com dados de Processamento de Uvas
def consultar_processamento_uva(tipo_de_uva: str = None, grupo_de_uva: str = None, nm_uva: str = None, ano: int = None):
    """Consulta os dados de processamento com filtros opcionais"""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT tipo_de_uva, grupo_de_uva, nm_uva, ano, quantidade_kg FROM processamento_uvas WHERE 1=1"
    params = []

    if tipo_de_uva:
        query += " AND tipo_de_uva = ?"
        params.append(tipo_de_uva)
    if grupo_de_uva:
        query += " AND grupo_de_uva = ?"
        params.append(grupo_de_uva)
    if nm_uva:
        query += " AND nm_uva LIKE ?"
        params.append(f"%{nm_uva}%")
    if ano:
        query += " AND ano = ?"
        params.append(ano)

    cursor.execute(query, params)
    dados = cursor.fetchall()
    conn.close()

    return [
        ProcessamentoUva(
            tipo_de_uva=row["tipo_de_uva"],
            grupo_de_uva=row["grupo_de_uva"],
            nm_uva=row["nm_uva"],
            ano=row["ano"],
            quantidade_kg=row["quantidade_kg"] if isinstance(row["quantidade_kg"], int) else 0  # Define um valor 0 se for None para não gerar erro na classe pq ela é do tipo int
        )
        for row in dados
    ]


#API Comercialização
def get_comercializacao(produto_principal=None, subproduto=None, ano=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM comercializacao_produtos WHERE 1=1"
    params = []

    if produto_principal:
        query += " AND produto_principal = ?"
        params.append(produto_principal)
    if subproduto:
        query += " AND subproduto = ?"
        params.append(subproduto)
    if ano:
        query += " AND ano = ?"
        params.append(ano)

    cursor.execute(query, params)
    dados = cursor.fetchall()
    conn.close()
    return [dict(row) for row in dados]

#API Exportacao
def get_exportacao(pais=None, ano=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM exportacao_produtos WHERE 1=1"
    params = []

    if pais:
        query += " AND pais = ?"
        params.append(pais)
    if ano:
        query += " AND ano = ?"
        params.append(ano)

    cursor.execute(query, params)
    dados = cursor.fetchall()
    conn.close()
    return [dict(row) for row in dados]

#API Importacao
def get_importacao(pais=None, ano=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM importacao_produtos WHERE 1=1"
    params = []

    if pais:
        query += " AND pais = ?"
        params.append(pais)
    if ano:
        query += " AND ano = ?"
        params.append(ano)

    cursor.execute(query, params)
    dados = cursor.fetchall()
    conn.close()
    return [dict(row) for row in dados]
