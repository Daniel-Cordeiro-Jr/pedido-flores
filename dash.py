# Carrega as bibliotecas
import streamlit as st
import pandas as pd

# Carrega a imagem do logo
st.image('logo.jpeg')

# Carrega a tabela com Mercadorias e Quantidades a serem trabalhadas
dftab = pd.read_excel('mercadoria.xlsx', sheet_name = 'pedido')

# Formata os campos da tabela de dados
dftab = dftab.astype({
    'cod_produto': 'str',
    'desc_produto': 'str',
    'quantidade1': 'str',
    'quantidade2': 'str',
    'quantidade3': 'str',
    'quantidade4': 'str',
    'pedido': 'str'
})

df_ini = dftab[['cod_produto', 'desc_produto', 'quantidade1', 'quantidade2', 'quantidade3', 'quantidade4']]

st.dataframe(df_ini, hide_index=True)

st.markdown(f"\t<h3 style='text-align: center; color: black;'>Guia de Pedidos</h3>", unsafe_allow_html=True)


# Criar uma lista vazia para armazenar as seleções
selecoes = []



# Criar um loop for para iterar sobre os produtos e as quantidades
for cod_prod, produto, q0, q1, q2, q3, q4 in zip(dftab['cod_produto'],dftab['desc_produto'], dftab['qtd0'], dftab['quantidade1'], dftab['quantidade2'], dftab['quantidade3'], dftab['quantidade4']):
    selecao = st.selectbox(f'Selecione a quantidade desejada de **{produto}**:', [q0, q1, q2, q3, q4], key=cod_prod)
    selecoes.append(selecao)
    
    # Exibir a lista de seleções
    soma = sum(int(i) for i in selecoes)
    
dftab['pedido'] = selecoes


st.markdown(f"\t<h3 style='text-align: center; color: black;'>PEDIDO</h3>", unsafe_allow_html=True)
df_final = dftab[['cod_produto', 'desc_produto', 'pedido']]
df_final = df_final[(dftab['pedido'] != 0)]
st.dataframe(df_final, hide_index=True)

st.write(f'Seu pedido tem um total de: {soma} itens')
