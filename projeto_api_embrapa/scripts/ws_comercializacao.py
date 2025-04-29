import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from datetime import datetime

# URL da base Embrapa para consulta de comercialização
BASE_URL_COMERCIALIZACAO = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04&ano={}"

# Lista de produtos principais da comercialização
PRODUTOS_COMERCIALIZACAO = [
    "VINHO DE MESA", "VINHO FINO DE MESA", "VINHO FRIZANTE", "VINHO ORGÂNICO",
    "VINHO ESPECIAL", "ESPUMANTES", "SUCO DE UVAS CONCENTRADO", "OUTROS PRODUTOS COMERCIALIZADOS"
]

# Conectar ao banco SQLite
conn = sqlite3.connect("data/database.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM producao_produtos") #Limpando a tabela para uma nova carga FULL

def get_comercializacao_data(year):
    """Coleta os dados de comercialização do site da Embrapa para o ano filtrado."""
    url = BASE_URL_COMERCIALIZACAO.format(year)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="tb_base tb_dados")

        if table:
            rows = table.find_all("tr")[1:]  # Ignora o cabeçalho
            produto_principal = None

            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    produto = cols[0].text.strip()
                    quantidade = cols[1].text.strip().replace(".", "")  # Remove pontos para conversão numérica

                    if "tb_item" in cols[0].get("class", []):
                        produto_principal = produto
                        subproduto = produto
                    elif "tb_subitem" in cols[0].get("class", []):
                        subproduto = produto

                    # Adicionar ao banco na tabela `comercializacao_produtos`
                    cursor.execute("INSERT INTO comercializacao_produtos (produto_principal, subproduto, quantidade_l, ano) VALUES (?, ?, ?, ?)",
                                   (produto_principal, subproduto, int(quantidade) if quantidade.isdigit() else None, year))
            
            conn.commit()
        else:
            print(f"Tabela não encontrada para {year}")
    else:
        print(f"Erro ao acessar {url}: Código {response.status_code}")

# Percorrer anos e coletar dados
for year in range(1970, datetime.now().year):
    get_comercializacao_data(year)

print("Banco de dados atualizado com comercialização!")