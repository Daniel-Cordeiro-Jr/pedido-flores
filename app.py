# Carrega as bibliotecas
import streamlit as st
import pandas as pd

# Carrega a imagem do logo
st.image('logo.jpeg')
st.markdown(f"\n")

# Carrega a tabela com Mercadorias e Quantidades a serem trabalhadas
dftab = pd.read_excel(f'mercadoria.xlsx')

# Formata os campos da tabela de dados
dftab = dftab.astype({'cod_produto': 'str', 'desc_produto': 'str',
                      'quantidade1': 'str', 'quantidade2': 'str',
                      'quantidade3': 'str', 'quantidade4': 'str', 'pedido': 'str'
})
lista_campos=['cod_produto','desc_produto','pedido']

campos=['cod_produto','desc_produto','quantidade1','quantidade2','quantidade3','quantidade4']

# Mostra a tabela mãe para apoio da seleção de quantidades
st.dataframe(dftab[campos], hide_index=True)

# Funcão para retornar as quantidades de cada produto no selectbox
def get_quantidades(produto):
    # Selecionar as colunas de quantidade e converter para uma lista
    quantidades = df_produto[['quantidade1', 'quantidade2', 'quantidade3', 'quantidade4']].values.tolist()[0]
    return quantidades

st.markdown(f"\n")
st.markdown(f"<h3 style='text-align: center; color: black;'>Guia de Pedidos</h3>", unsafe_allow_html=True)

# Selecionar o produto desejado
selecao_prod=st.selectbox(f'****Produtos Disponíveis:****',dftab['desc_produto'],
                                                         placeholder="Selecione o produto...",
                                                         index=True
                                                        )
# Cria um dataframe filtrando o produto selecionado
df_produto = dftab.loc[dftab['desc_produto'] == selecao_prod]

# Selecionar as quantidades desejadas
selecao_qtd=st.selectbox(f'****Quantidades Disponíveis:****', [*get_quantidades(selecao_prod)],
                                                         placeholder="Selecione a quantidade...",
                                                         index=True
                                                         )
# Extrai o codigo do produto
codproduto = df_produto.loc[df_produto['desc_produto'] == selecao_prod, 'cod_produto'].values[0]

# Insere o valor selecionado no datafreme
dftab.loc[dftab['cod_produto'] == codproduto, 'pedido'] = selecao_qtd


# Exibir somantório de quantidades
if dftab[dftab['pedido'].notnull()].empty == False:
    soma = pd.to_numeric(dftab['pedido'], errors='coerce').sum()

st.markdown(f"\n")
st.markdown(f"\t<h3 style='text-align: center; color: black;'>Pedido</h3>", unsafe_allow_html=True)
df_final = dftab[(dftab['pedido'] != "nan")]

# Cria botão enviar Pedido(em construção)
if st.button("Enviar Pedido"):
    df_final = None
st.dataframe(df_final[lista_campos], hide_index=True)
st.write(f'Seu pedido tem um total de: {int(soma.round(0))} itens')
# Cria botão para limpar Pedido(em construção)
if st.button("Limpar"):
    df_final = None



