# Carrega as bibliotecas
import streamlit as st
import pandas as pd

# Carrega a imagem do logo
st.image('logo.jpeg')
st.markdown(f"\n")

# Carrega a tabela com Mercadorias e Quantidades a serem trabalhadas
dftab = pd.read_excel(f'mercadoria.xlsx')
original_df=dftab.copy()

# Formata os campos da tabela de dados
dftab = dftab.astype({'cod_produto': 'str', 'desc_produto': 'str',
                      'quantidade1': 'str', 'quantidade2': 'str',
                      'quantidade3': 'str', 'quantidade4': 'str', 'pedido': 'str'
})
colunas=['cod_produto','desc_produto','quantidade1','quantidade2','quantidade3','quantidade4']

# Cria dataframe de pedidos
colunapedido=['cod_produto','desc_produto','pedido']
dfpedido = pd.DataFrame(columns=colunapedido)

# Mostra a tabela mãe para apoio da seleção de quantidades
#st.dataframe(dftab[colunas], hide_index=True)

# Funcão para retornar as quantidades de cada produto no selectbox
def get_quantidades(produto):
    # Selecionar as colunas de quantidade e converter para uma lista
    quantidades = dftab[['quantidade1', 'quantidade2', 'quantidade3', 'quantidade4']].values.tolist()[0]
    return quantidades

# Funcão para atualizar dados no Dataframe
def atualiza_dftab(produto,quantidade):
    # Extrai o codigo do produto
    codproduto = dftab.loc[dftab['desc_produto'] == selecao_prod, 'cod_produto'].values[0]
    #mask = (dftab['cod_produto'].values)
    #dftab.loc[dftab['cod_produto'] == codproduto, 'pedido'] = quantidade
    selecao=[codproduto,produto,quantidade]
    dfpedido.loc[len(dfpedido)] = selecao

st.markdown(f"\n")
st.markdown(f"<h3 style='text-align: center; color: black;'>Guia de Pedidos</h3>", unsafe_allow_html=True)

# Selecionar o produto desejado
selecao_prod=st.selectbox(f'****Produtos Disponíveis:****',dftab['desc_produto'],
                                                         placeholder="Selecione o produto...",index=None)

# Selecionar as quantidades desejadas
selecao_qtd=st.selectbox(f'****Quantidades Disponíveis:****', [*get_quantidades(selecao_prod)],
                                                            placeholder="Selecione a quantidade...",index=None)

# Chama função que insere os valores selecionados no datafreme
atualiza_dftab(selecao_prod,selecao_qtd)

# Somantório de quantidades
soma = pd.to_numeric(dfpedido['pedido'], errors='coerce').sum()

st.markdown(f"\n")
st.markdown(f"\t<h3 style='text-align: center; color: black;'>Pedido</h3>", unsafe_allow_html=True)

# Cria botão enviar Pedido(em construção)
#if st.button("Enviar Pedido"):
#    df_final = None
df_pedido = dftab[dftab['pedido'] != "nan"]
st.dataframe(dfpedido, hide_index=True)
st.write(f'Seu pedido tem um total de: {int(soma.round(0))} itens')
# Cria botão para limpar Pedido(em construção)
#if st.button("Limpar"):
#    df_final = None
