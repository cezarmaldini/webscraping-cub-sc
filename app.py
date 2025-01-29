import requests # Biblioteca para fazer requisição em url
from bs4 import BeautifulSoup # Biblioteca para ler html
import pandas as pd # Pandas hahaha
from sqlalchemy import create_engine # Biblioteca para criar conexão com o Banco de Dados PostgreSQL
from sqlalchemy.sql import text # Biblioteca para executar Query no Banco de Dados SQL
import locale # Definir localização geográfica
import os
from dotenv import load_dotenv

# Define o locale para português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# Acessando o site e buscando código HTML
def html_page():
    url = 'https://sinduscon-fpolis.org.br/servico/cub-mensal/#1lsUT6V6fB3QTot-pyShEhnK9RLOOuGn0'
    response = requests.get(url)
    return response.text

def data_page(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Captura o Mês
    mes = soup.find('strong', text="Para ser usado em:")
    mes_text = mes.find_next('span').get_text(strip=True) if mes else 'Não encontrado'

    # Captura o valor do CUB
    cub_ref_element = soup.find('div', class_="us_custom_eb849559")
    cub_ref_text = cub_ref_element.find('span', style="color: #9e3d42;").get_text(strip=True) if cub_ref_element else 'Não encontrado'

    # Cria e retorna o DataFrame
    data = {
        'mes': [mes_text],
        'cub_ref': [cub_ref_text]
    }

    df = pd.DataFrame(data)

    # Converte a coluna 'mes' para uma data no formato 01/MM/AAAA
    df['mes'] = pd.to_datetime(df['mes'], format='%B/%Y')  # Converte em datetime
    df['mes'] = df['mes'].dt.strftime('%d/%m/%Y %H:%M:%S')  # Ajusta o formato

    return df

def convert_to_float(value):
    # Remove o separador de milhar (ponto) e substitui a vírgula pelo ponto decimal
    return float(value.replace('.', '').replace(',', '.'))

def insert_data(df, db_url, table_name):
    # Cria a conexão com o banco
    engine = create_engine(db_url)

    with engine.connect() as connection:
        # Começa uma transação
        with connection.begin():
            for _, row in df.iterrows():
                # Converte o valor do CUB para float
                cub_value = convert_to_float(row['cub_ref'])

                # Garante que a data esteja no formato aceito pelo PostgreSQL (timestamp)
                data_formatada = pd.to_datetime(row['mes'], format='%d/%m/%Y %H:%M:%S')

                # Query para verificar se a data já existe
                query = text(f"SELECT COUNT(*) FROM {table_name} WHERE \"Data\" = :data")
                result = connection.execute(query, {"data": data_formatada}).scalar()

                # Se não existir, insere os dados
                if result == 0:
                    insert_query = text(f"""
                    INSERT INTO {table_name} ("Data", "CUB")
                    VALUES (:data, :cub)
                    """)
                    connection.execute(insert_query, {"data": data_formatada, "cub": cub_value})
                    print(f"Dados inseridos: {data_formatada}, {cub_value}")
                else:
                    print(f"Dados já existem no banco para a data {data_formatada}.")

            # O commit da transação acontece automaticamente aqui ao sair do bloco with

# Função principal
def main():
    # Parâmetros de conexão
    db_url = os.getenv('DB_URL')
    table_name = "cub"

    # Obtenção e processamento da página
    html = html_page()
    df = data_page(html)

    # Inserir no banco se não existir
    insert_data(df, db_url, table_name)

# Executa o script
if __name__ == "__main__":
    main()