import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from datetime import datetime

# URL base para importação
BASE_URL_IMPORTACAO = "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao={}&opcao=opt_05&ano={}"
 
# Filtros disponíveis para importação
FILTROS_IMPORTACAO = {
    "Vinhos de mesa": "subopt_01",
    "Espumantes": "subopt_02",
    "Uvas frescas": "subopt_03",
    "Uvas passas": "subopt_04",
    "Suco de uva": "subopt_05"
}

# Criar conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect("C:\\Users\\Gabriel\\Desktop\\FIAP\\Tech Challeng FIAP\\projeto_api_embrapa\\data\\database.db")
    conn.row_factory = sqlite3.Row
    return conn

def extrair_dados_importacao():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM importacao_produtos")  # Limpando a tabela para nova carga FULL
    print("Tabela importação limpa e pronta para nova carga FULL.")

    for ano in range(1970, datetime.now().year):  # De 1970 até o ano atual
        for nome_filtro, filtro in FILTROS_IMPORTACAO.items():
            url = BASE_URL_IMPORTACAO.format(filtro, ano)
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Erro ao acessar {url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for linha in soup.select("table.tb_base tbody tr"):   
                colunas = linha.find_all("td")
                pais = colunas[0].text.strip()
                quantidade = colunas[1].text.strip().replace(".", "").replace(",", "").strip()
                valor = colunas[2].text.strip().replace(".", "").replace(",", "").strip()
                
                # Remover possíveis caracteres não numéricos e tratar valores ausentes
                quantidade_kg = int(quantidade) if quantidade.isdigit() else None
                valor_usd = float(valor) if valor.replace(".", "").isdigit() else None
                
                cursor.execute("""
                INSERT INTO importacao_produtos (pais, quantidade_kg, valor_usd, ano, tipo_de_uva)
                VALUES (?, ?, ?, ?, ?)
                """, (pais, quantidade_kg, valor_usd, ano, nome_filtro))

            conn.commit()
            print(f"Dados de {nome_filtro} ({ano}) inseridos!")

            time.sleep(1)  # Evita sobrecarga no servidor

    conn.close()
    print("Extração da base de importações finalizada!")
# Executando o script
extrair_dados_importacao()