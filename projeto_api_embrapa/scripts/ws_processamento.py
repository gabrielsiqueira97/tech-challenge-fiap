import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from datetime import datetime

# URL base
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao={}&opcao=opt_03&ano={}"

# Filtros disponíveis
FILTROS_UVAS = {
    "Viníferas": "subopt_01",
    "Americanas e híbridas": "subopt_02",
    "Uvas de mesa": "subopt_03",
    "Sem classificação": "subopt_04"
}

# Criar conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect("C:\\Users\\Gabriel\\Desktop\\FIAP\\Tech Challeng FIAP\\projeto_api_embrapa\\data\\database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Extrair dados
def extrair_dados_processamento():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM processamento_uvas") #Limpando a base de dados para uma carga FULL
    print("Tabela limpa pronta para nova carga FULL")
    
    for ano in range(1970, datetime.now().year):  # De 1970 até o ano atual
        for nome_filtro, filtro in FILTROS_UVAS.items():
            url = BASE_URL.format(filtro, ano)
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Erro ao acessar {url}")
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            grupo_atual = None
            
            for linha in soup.select("table.tb_dados tbody tr"):
                colunas = linha.find_all("td")
                
                if "tb_item" in colunas[0].get("class", []):  # É o grupo de uvas (TINTAS, BRANCAS...)
                    grupo_atual = colunas[0].text.strip()
                
                elif "tb_subitem" in colunas[0].get("class", []):  # Nome da uva
                    nm_uva = colunas[0].text.strip()
                    quantidade = colunas[1].text.strip()
                    quantidade = quantidade.replace(".", "").replace(",", "")  # Remove formatação para tranformar em numero
                    quantidade = int(quantidade) if quantidade.isdigit() else None
                    cursor.execute("""
                    INSERT INTO processamento_uvas (tipo_de_uva, grupo_de_uva, nm_uva, ano, quantidade_kg)
                    VALUES (?, ?, ?, ?, ?)
                    """, (nome_filtro, grupo_atual, nm_uva, ano, quantidade))

            conn.commit()
            print(f"Dados de {nome_filtro} ({ano}) inseridos!")

            time.sleep(1)  # Evita sobrecarga no servidor

    conn.close()
    print("🚀 Extração finalizada!")

# Executando o script
extrair_dados_processamento()