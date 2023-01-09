#########Importing Libraries#########

from sqlalchemy  import create_engine
from bs4         import BeautifulSoup
from datetime    import datetime

import sqlite3
import requests
import pandas as pd
import numpy as np
import re
import logging
import os

#########Utils#########

def get_colors_and_composition(id):
    #url em que a requisição será feita
    url_model = f'https://www2.hm.com/en_us/productpage.{id}.html'

    #fazendo a requisição
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    page = requests.get(url_model, headers=headers)

    #pegando o html da página
    html = page.text

    #criando um objeto do BeautifulSoup a partir do html
    soup_product = BeautifulSoup(html)
    
    # ====================colors===========================
    
    #pegando todos os tipos de cores
    product_colors = soup_product.find('ul', class_='inputlist clearfix')

    if product_colors == None:
        return "Unknown", "Unknown", "Unknown"
    
    #cores disponíveis daquele produto
    colors = [product_item.find('a').get('data-color') for product_item in product_colors.find_all('li', class_='list-item')]
    
    # ====================composition===========================
    attributes = list(filter(None, soup_product.find('div', class_='content pdp-text pdp-content').get_text().split('\n')))

    for i in range(len(attributes)):
        if attributes[i] == 'Composition':
                composition_shell = attributes[i+1]
                composition_pocket = attributes[i+2]
    
    
    return "//".join(colors), composition_shell, composition_pocket


#########Data Collection#########
#########Job1#########

def data_collection(url, headers):
    #fazendo a requisição para pegar o html da vitrine
    page = requests.get(url, headers=headers)

    #pegando o html da página
    html = page.text

    #criando um objeto a partir do html
    soup = BeautifulSoup(html, 'html.parser')

    #coletando quantos items existem ao total
    total_items = int(soup.find('h2', class_='load-more-heading').get('data-total'))

    #considerando que cada página mostra 36 produtos, vemos quantas paginas precisam
    page_number = int(round(total_items/36))

    #url para pegar todos os produtos
    url2 = url + "?page-size=" + str(page_number*36)

    #fazendo a requisição
    page = requests.get(url2, headers=headers)

    #pegando o html da página
    html = page.text

    #criando um objeto do BeautifulSoup a partir do html
    soup_pagination = BeautifulSoup(html)

    ############################
    #####Nome, tipo e preço#####
    ############################

    #buscando pela lista que contém todos produtos
    all_products = soup_pagination.find('ul', class_='products-listing small')

    #fazendo uma lista que tem o html de cada produto
    products_list = all_products.find_all('article', class_='hm-product-item')

    #listas para armazenar tipo e preço de cada produto
    products_id, products_type, products_price, products_name = [],[],[],[]

    #iterando em todos os produtos e pegando preço e tipo
    for product in products_list:
        product_details = product.find('div', class_='item-details')
        products_id.append(product.get('data-articlecode'))
        products_type.append(product.get('data-category'))
        products_price.append(product_details.find('span', class_='price regular').get_text())
        products_name.append(product_details.find('a', class_='link').get_text())

    #criando um dataframe com os dados coletando até agora
    df = pd.DataFrame([products_id, products_name, products_type, products_price]).T
    df.columns = ['product_id', 'product_name', 'product_type', 'product_price']
    df['scrapy_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df


#########Job2#########

def data_collection_by_product(df):
    ############################
    #####Cores e composição#####
    ############################

    #lista para armazenar as cores 
    products_colors = []

    #lista para armazenar a composição
    products_composition_shell = []
    products_composition_pocket = []

    #para cada produto pegar as cores e composição e adicionar na lista
    for id in df['product_id']:
        colors, composition_shell, composition_pocket = get_colors_and_composition(id)
        products_colors.append(colors)
        products_composition_shell.append(composition_shell)
        products_composition_pocket.append(composition_pocket)    

    #adiciona as colunas de cores e composição do produto no dataframe
    df["product_colors"] = products_colors
    df["product_composition_shell"] = products_composition_shell
    df["product_composition_pocket"] = products_composition_pocket

    return df


#########Data Cleaning#########
#########Job3#########

def data_cleaning(df):

    #reordenando as colunas
    df = df[["product_id", "product_name", "product_type", "product_colors", "product_price", "product_composition_shell", "product_composition_pocket", "scrapy_datetime"]]

    #se a string não começar com "Poc" significa que esse valor não estava presente no site
    df["product_composition_pocket"] = df["product_composition_pocket"].apply(lambda x: x if x[:3] == "Poc" else np.nan)

    #limpando as colunas de composição do produto
    df["product_composition_shell"] = df['product_composition_shell'].str.replace('Shell: ', '')
    df["product_composition_pocket"] = df['product_composition_pocket'].str.replace('Pocket lining: ', '')
    df["product_composition_pocket"] = df['product_composition_pocket'].str.replace('Pocket: ', '')

    #######uma linha por produto-cor########

    #dataframe final
    df_raw = pd.DataFrame()

    #para cada produto do df, extrai as cores e cria uma linha pra cada cor
    for i in range(len(df)):
        #pega a linha
        df_row = pd.DataFrame(df.loc[i]).T
        #pega as cores daquele produto
        unique_colors = df_row["product_colors"].values[0].split("//")
        
        #pra cada cor, cria uma nova linha
        for i in range(len(unique_colors)):
            df_row["product_colors"] = unique_colors[i]
            df_raw = pd.concat([df_raw, df_row])

    ##########limpeza geral############

    #copiando o dataframe raw
    df_raw = df_raw.reset_index(drop=True)
    df = df_raw.copy()

    #######product_name##########
    df["product_name"] = df["product_name"].apply(lambda x: x.replace(" ", "_").lower())

    ######product_colors#########
    df["product_colors"] = df["product_colors"].apply(lambda x: x.replace(" ", "_").lower())

    ######product_price##########
    df["product_price"] = df["product_price"].apply(lambda x: x.replace("$", "").strip())
    df["product_price"] = df["product_price"].astype(float)

    #####product_composition_shell#####

    # dataframe auxiliar
    df_aux = df.product_composition_shell.str.split(",", expand=True)

    # criar um dataframe de referência
    df_ref = pd.DataFrame(index=np.arange(len(df)), columns=["cotton", "spandex", 
                                                            "elastomultiester", "polyester", "lyocell", "rayon"])

    #cotton
    df_cotton = df_aux[0].apply(lambda x: x if "Cotton" in x else np.nan)
    df_cotton = df_cotton.reset_index(drop=True)
    df_cotton.name = "cotton"

    df_ref = pd.concat([df_ref, df_cotton], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    #spandex
    df_spandex = pd.Series(dtype=str)

    df_aux = df_aux.fillna("string vazia")

    for i in df_aux.index:
        spandex_in_1 = "Spandex" in df_aux.loc[i][1]
        spandex_in_2 = "Spandex" in df_aux.loc[i][2]
        if spandex_in_1:
            df_spandex.loc[i] = df_aux.loc[i][1]
        elif spandex_in_2:
            df_spandex.loc[i] = df_aux.loc[i][2]
        else:
            df_spandex.loc[i] = np.nan
            
    df_spandex.name = "spandex"

    df_ref = pd.concat([df_ref, df_spandex], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    #elastomultiester
    df_elastomultiester = pd.Series(dtype=str)

    for i in df_aux.index:
        elastomultiester_in_1 = "Elastomultiester" in df_aux.loc[i][1]
        if elastomultiester_in_1:
            df_elastomultiester.loc[i] = df_aux.loc[i][1]
        else:
            df_elastomultiester.loc[i] = np.nan

    df_elastomultiester.name = "elastomultiester"

    df_ref = pd.concat([df_ref, df_elastomultiester], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    #polyester
    df_polyester = pd.Series(dtype=str)

    for i in df_aux.index:
        polyester_in_1 = "Polyester" in df_aux.loc[i][1]
        if polyester_in_1:
            df_polyester.loc[i] = df_aux.loc[i][1]
        else:
            df_polyester.loc[i] = np.nan
            
    df_polyester.name = "polyester"

    df_ref = pd.concat([df_ref, df_polyester], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    #lyocell
    df_lyocell = pd.Series(dtype=str)

    for i in df_aux.index:
        lyocell_in_0 = "Lyocell" in df_aux.loc[i][0]
        lyocell_in_1 = "Lyocell" in df_aux.loc[i][1]
        if lyocell_in_0:
            df_lyocell.loc[i] = df_aux.loc[i][0]
        elif lyocell_in_1:
            df_lyocell.loc[i] = df_aux.loc[i][1]
        else:
            df_lyocell.loc[i] = np.nan
            
    df_lyocell.name = "lyocell"

    df_ref = pd.concat([df_ref, df_lyocell], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    #rayon
    df_rayon = pd.Series(dtype=str)

    for i in df_aux.index:
        rayon_in_0 = "Rayon" in df_aux.loc[i][0]
        rayon_in_2 = "Rayon" in df_aux.loc[i][2]
        if rayon_in_0:
            df_rayon.loc[i] = df_aux.loc[i][0]
        elif rayon_in_2:
            df_rayon.loc[i] = df_aux.loc[i][2]
        else:
            df_rayon.loc[i] = np.nan
            
    df_rayon.name = "rayon"

    df_ref = pd.concat([df_ref, df_rayon], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    #joining df_ref and df
    df = pd.concat([df, df_ref], axis=1)

    #drop product_composition column
    df = df.drop("product_composition_shell", axis=1)

    #get only the number composition
    columns_composition = df_ref.columns
    for column in columns_composition:
        df[column] = df[column].apply(lambda x: int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)    

    ########product_composition_pocket########

    #drop product_composition_pocker because what really matter is the shell
    df = df.drop("product_composition_pocket", axis=1)


    ########scrapy_datetime#########

    #reordering the columns
    column_order = ['product_id', 'product_name', 'product_type', 'product_colors',
        'product_price', 'cotton', 'spandex',
        'elastomultiester', 'polyester', 'lyocell', 'rayon', 'scrapy_datetime']

    df = df[column_order]

    #convert to datetime type
    df["scrapy_datetime"] = pd.to_datetime(df["scrapy_datetime"], format="%Y-%m-%d %H:%M:%S")


    ########Final Dataframe#######

    #dropping duplicates
    df = df.drop_duplicates()

    #reseting index
    df = df.reset_index(drop=True)

    #fillna with 0, meaning that it doesn't compose the product
    df = df.fillna(0)

    return df


#########Data Insert#########
#########Job4#########

def data_insert(df):

    #conectando ao banco de dados
    conn = create_engine('sqlite:///database_hm.sqlite', echo=False)

    #populando a tabela com dados do dataframe
    df.to_sql(
        'showroom',
        con=conn,
        if_exists='append',
        index=False
    )


if __name__ == "__main__":
    #logging
    path = "C:/Users/allan/Documents/GitHub/python_ds_ao_dev/etl/"

    if not os.path.exists(path + "Logs"):
        os.makedirs(path + "Logs")

    logging.basicConfig(
        filename= path + "Logs/webscrapping_hm.log",
        level= logging.DEBUG,
        format= "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt= "%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger("webscrapping_hm")

    #parameters and constants
    url = 'https://www2.hm.com/en_us/men/products/jeans.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

    logger.info("script started running")

    #data collection
    data = data_collection(url, headers)
    logger.info("data collection done")

    #data collection by product
    final_data = data_collection_by_product(data)
    logger.warning("could add a log in each product to monitor when the script stopped")
    logger.info("data collection by product done")

    #data cleaning
    cleaned_data = data_cleaning(final_data)
    logger.info("data cleaning done")

    #data insert
    data_insert(cleaned_data)
    logger.info("data insertion done")

    logger.info("script finished")
