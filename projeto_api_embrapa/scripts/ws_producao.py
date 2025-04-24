import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL da base embrapa para consulta
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano={}"

# Lista de produtos principais
PRODUTOS_PRINCIPAIS = ["VINHO DE MESA", "VINHO FINO DE MESA (VINIFERA)", "SUCO", "DERIVADOS"]

# Conectar ao banco SQLite
conn = sqlite3.connect("data/database.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM producao_produtos") #Limpando a tabela para uma nova carga FULL

def get_production_data(year):
    """Coleta os dados de produção do site da Embrapa para o ano filtrado."""
    url = BASE_URL.format(year)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="tb_base tb_dados")
        data = []

        if table:
            rows = table.find_all("tr")[1:]  # Ignora o cabeçalho
            produto_principal = None  # Para rastrear o produto principal atual

            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    produto = cols[0].text.strip()
                    quantidade = cols[1].text.strip().replace(".", "")  # Remove pontos para conversão numérica

                    # Verifica se o elemento é um produto principal ou subproduto
                    if "tb_item" in cols[0].get("class", []):
                        produto_principal = produto  # Define o produto principal
                        subproduto = produto  # Se for principal, ele mesmo será o subproduto
                    elif "tb_subitem" in cols[0].get("class", []):
                        subproduto = produto  # Caso seja um subproduto

                    # Adicionar ao banco na tabela `producao_produtos`
                    cursor.execute("INSERT INTO producao_produtos (produto_principal, subproduto, quantidade, ano) VALUES (?, ?, ?, ?)",
                                   (produto_principal, subproduto, int(quantidade) if quantidade.isdigit() else None, year))
            
            conn.commit()
        else:
            print(f"Tabela não encontrada para {year}")
    else:
        print(f"Erro ao acessar {url}: Código {response.status_code}")

# Percorrer anos de 1970 a 2023 e coletar dados
for year in range(1970, datetime.now().year):
    get_production_data(year)

# Fechar conexão
conn.close()

print("Banco de dados atualizado")