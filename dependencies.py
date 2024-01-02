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
    connection = psycopg2.connect(database=DATABAE, user=USERSERVER, password=PASSWORD, host=HOST, port=PORT)
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
            st.markdown(f"Pedido gravado e enviado com sucesso!")    
    except (Exception, psycopg2.DatabaseError) as error:
        st.markdown(f"Erro ao inserir registros: {str(error)}")