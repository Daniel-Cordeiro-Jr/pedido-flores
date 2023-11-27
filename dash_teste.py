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
                      'minimo': 'str', 'qtd2': 'str',
                      'qtd3': 'str', 'qtd4': 'str', 'pedido': 'str'
})

def get_quantidades(codigo):
    # Selecionar as colunas de quantidade e converter para uma lista
    if codigo:
        quantidades = None
        quantidades = dftab.loc[dftab['cod_produto'] == codigo, ['minimo','qtd2','qtd3','qtd4']].values[0]
        #quantidades = dftab[['quantidade1', 'quantidade2', 'quantidade3', 'quantidade4']].values.tolist()[0]
        return quantidades

if 'num' not in st.session_state:
    st.session_state.num = 1
if 'data' not in st.session_state:
    st.session_state.data = []

class NovoPedido:
    def __init__(self, page_id):
        # Selecionar o produto desejado
        selecao_prod=st.selectbox(f'****Produtos Disponíveis:****',dftab['desc_produto'],
                                                         placeholder="Selecione o produto...")
        # Extrai o codigo do produto
        #if selecao_prod:
        codproduto = dftab.loc[dftab['desc_produto'] == selecao_prod, 'cod_produto'].values[0]

        # Selecionar as quantidades desejadas
        selecao_qtd=st.selectbox(f'****Quantidades Disponíveis:****', [*get_quantidades(codproduto)],
                                                            placeholder="Selecione a quantidade...")
        self.codproduto=codproduto
        self.produto = selecao_prod
        self.quantidade = selecao_qtd

def main():
    placeholder = st.empty()
    placeholder2 = st.empty()

    while True:
        num = st.session_state.num
        if placeholder2.button('Enviar Pedido', key=num):
            placeholder2.empty()
            dfpedido = pd.DataFrame(st.session_state.data)
            dfpedido = dfpedido.drop_duplicates(subset='Produto').reset_index(drop=True)
            st.dataframe(dfpedido, hide_index=True)
            break
        else:
           with placeholder.form(key=str(num)):
               new_produto = NovoPedido(page_id=num)
               if st.form_submit_button('Adicionar'):
                   st.session_state.data.append({
                       'Codigo': new_produto.codproduto,
                       'Produto': new_produto.produto,
                       'Quantidade': new_produto.quantidade
                   })
                   dfpedido = pd.DataFrame(st.session_state.data)
                   dfpedido = dfpedido.drop_duplicates(subset='Produto').reset_index(drop=True)
                   st.dataframe(dfpedido, hide_index=True)
                   st.session_state.num += 1
                   placeholder.empty()
                   placeholder2.empty()
               else:
                   st.stop()
main()