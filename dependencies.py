import os
import psycopg2
import streamlit as st
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

DATABAE = os.getenv("DATABAE")
HOST = os.getenv("HOST")
USERSERVER = os.getenv("USERSERVER")
PASSWORD = os.getenv("PASSWORD")
PORT = int(os.getenv("PORT"))

@contextmanager
def instance_cursor():
    connection = psycopg2.connect(database=DATABAE, user=USERSERVER, password=PASSWORD, host=HOST, port=5432)
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        if (connection):
            cursor.close()
            connection.close()

def insere_registros(dfpedido):
    try:
        connection = psycopg2.connect(database=DATABAE, user=USERSERVER, password=PASSWORD, host=HOST, port=5432)
        cursor = connection.cursor()
        query = """
        INSERT INTO tb_pedidos(nun_loja, 
                               desc_loja, 
                               dt_pedido, 
                               cod_produto, 
                               desc_produto, 
                                quantidade,
                                dt_entrega) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for index, row in dfpedido.iterrows():
            cursor.execute(query, (row['nun_loja'], row['desc_loja'], row['dt_pedido'],row['cod_produto'], row['desc_produto'], row['quantidade'], row['dt_entrega']))
            connection.commit()
        if (connection):
            cursor.close()
            connection.close()
            st.markdown(f"\t<h6 style='text-align: CENTER; color: with;'># Pedido gravado e enviado com sucesso! #</h6>", unsafe_allow_html=True)  
    except (Exception, psycopg2.DatabaseError) as error:
        st.markdown(f"Erro ao inserir registros: {str(error)}")


def consulta_rede():
    connection = psycopg2.connect(database=DATABAE, user=USERSERVER, password=PASSWORD, host=HOST, port=5432)
    cursor = connection.cursor()
    with instance_cursor() as cursor:
        query = """ 
            select rede from tb_rede_tabela
            order by 1;
            """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def consulta_loja(rede):
    connection = psycopg2.connect(database=DATABAE, user=USERSERVER, password=PASSWORD, host=HOST, port=5432)
    cursor = connection.cursor()
    with instance_cursor() as cursor:
        query = f""" 
            select pl.loja, pl.tabela 
            from tb_produtos_loja pl, tb_rede_tabela rt
            where rt.rede = '{rede}'
            and pl.tabela=rt.tabela
            order by 1;
            """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def consulta_produto(tabela):
    connection = psycopg2.connect(database=DATABAE, user=USERSERVER, password=PASSWORD, host=HOST, port=5432)
    cursor = connection.cursor()
    with instance_cursor() as cursor:
        query = f""" 
            select cod_produto, desc_produto 
            from tb_produtos
            where {tabela} = 1
            order by 1;
            """
        cursor.execute(query)
        produtos = cursor.fetchall()
        return produtos