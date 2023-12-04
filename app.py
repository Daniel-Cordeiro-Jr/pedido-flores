import streamlit as st
import pandas as pd

# Carrega a imagem do logo
st.image('logo.jpeg')
st.markdown(f"\n")

# Carrega a tabela com Mercadorias e Quantidades a serem trabalhadas
dftab = pd.read_excel(f'mercadoria.xlsx')

dftab.index = pd.RangeIndex(start=1, stop=len(dftab) + 1)

# Formata os campos da tabela de dados
dftab = dftab.astype({'cod_produto': 'str', 'desc_produto': 'str',
                      'minimo': 'str', 'qtd2': 'str',
                      'qtd3': 'str', 'qtd4': 'str'
})

st.markdown(f"\n")

def get_quantidades(codigo):
    # Selecionar as colunas de quantidade e converter para uma lista
    if codigo:
        quantidades = None
        quantidades = dftab.loc[dftab['cod_produto'] == codigo, ['minimo','qtd2','qtd3','qtd4']].values[0]
        return quantidades

#def exporta_pedido(dfpedido):
#    dfpedido.to_csv("pedido_loja.csv", index=False, header=False)

if 'num' not in st.session_state:
    st.session_state.num = 0
if 'data' not in st.session_state:
    st.session_state.data = []
class NovoPedido:
    def __init__(self, page_id):
        idx_produto = page_id
        idx_quantidade = 0
        self.produto = self.selecionaproduto(idx_produto)
        self.codigo = self.retorna_codigo(self.produto)

    def selecionaproduto(self, idx_produto):
        produto = st.selectbox(f'****Produtos Disponíveis:****', dftab['desc_produto'],
                               index=idx_produto,
                               placeholder="Selecione o produto...")
        return produto

    def retorna_codigo(self, selecao_prod):
        codigo = dftab.loc[dftab['desc_produto'] == selecao_prod, 'cod_produto'].values[0]
        return codigo

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
            exporta_pedido(dfpedido) 
            st.session_state.num = 1
            st.session_state.data = []         
            break
        else:
           with placeholder.form(key=str(num)):
               novo_produto = NovoPedido(page_id=num)
               quantidade=st.text_input(label='****Insira a Quantidade Desejada****')
               if st.form_submit_button('Adicionar'):
                   st.session_state.data.append({
                       'Codigo': novo_produto.codigo,
                       'Produto': novo_produto.produto,
                       #'Quantidade': novo_produto.quantidade
                       'Quantidade': quantidade
                   })
                   dfpedido = pd.DataFrame(st.session_state.data)
                   dfpedido = dfpedido.drop_duplicates(subset='Produto').reset_index(drop=True)
                   st.dataframe(dfpedido, hide_index=True)
                   st.session_state.num += 1
               else:
                   st.stop()        
main()
if st.button('Novo Pedido'):
    st.experimental_rerun()
