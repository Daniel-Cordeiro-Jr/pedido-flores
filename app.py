#Versão com tabelas sem Excel.


import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import sqlalchemy as sa
import datetime as dt
import psycopg2 as pg
import datetime as dt
from datetime import datetime
from PIL import Image
import os
from dependencies import insere_registros, consulta_loja, consulta_produto

# Carregar o arquivo style.css
with open ("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega a imagem do logo
st.image('logo.jpeg', use_column_width = True)


# Carrega a tabela Loja
loja=consulta_loja()
dftabloja = pd.DataFrame(loja, columns = ['LOJA', 'TABELA'])

def mostra_imagem(codigo):
    # Diretório onde as imagens estão armazenadas
    diretorio_imagens = "Imagens"
    # Abre a imagem selecionada
    #imagem = Image.open(os.path.join(diretorio_imagens, str(codigo) + ".jpeg"))
    try:
        imagem = Image.open(os.path.join(diretorio_imagens, str(codigo) + ".jpeg"))
        # Formatando imagem
        st.markdown("""<style>img {border: 4px solid green;}</style>""", unsafe_allow_html=True)
        # Mostra a imagem no Streamlit
        st.image(imagem)
    except IOError:
        st.markdown(f"\t<h5 style='text-align: center; color: with;'># Imagem não disponível! #</h5>", unsafe_allow_html=True)

def selecionaloja():
#Selecionar a Loja
    dftabloja = pd.DataFrame(loja, columns = ['LOJA', 'TABELA'])
    mensagem = "Selecione a Loja..."
    selected_option = st.selectbox(f'****Loja:****', dftabloja['LOJA'],
                               index = None, 
                               placeholder=mensagem)
    if selected_option == None:
        st.stop()
    else:
        tabela = dftabloja.loc[dftabloja['LOJA'] == selected_option, 'TABELA'].iat[0]

    return selected_option, tabela

def dt_pedido_quarta(data_atual):
    # Calcular o número de dias até a próxima sexta-feira
    dias_ate_quarta = (2 - data_atual.weekday()) % 7
    # Calcular a data da próxima sexta-feira
    proxima_quarta = data_atual + dt.timedelta(days=dias_ate_quarta + 7)
    # Formatar o objeto datetime para o formato desejado
    data_formatada = proxima_quarta.strftime('%d-%m-%Y')
    return data_formatada

def dt_pedido_sexta(data_atual):
    if data_atual.weekday() == 4:
        data_atual = data_atual + dt.timedelta(days=7)
    # Calcular o número de dias até a próxima sexta-feira
    dias_ate_sexta = (4 - data_atual.weekday()) % 7
    # Calcular a data da próxima sexta-feira
    proxima_sexta = data_atual + dt.timedelta(days=dias_ate_sexta)
    # Formatar o objeto datetime para o formato desejado
    data_formatada = proxima_sexta.strftime('%d-%m-%Y')
    return data_formatada

if 'num' not in st.session_state:
    st.session_state.num = 0
if 'data' not in st.session_state:
    st.session_state.data = []
class NovoPedido:
    def __init__(self, tabela, page_id, dftab, ):
        self.tabela = tabela
        self.page_id = page_id
        self.dftab = dftab
        self.produto = self.selecionaproduto(page_id)
        self.codigo = self.retorna_codigo(self.produto)

    def selecionaproduto(self, page_id):
        produto = st.selectbox(f'****Produto:****', self.dftab['desc_produto'],
                               index=page_id,
                               placeholder="Selecione o produto...")
        return produto
    
    def retorna_codigo(self, selecao_prod):
        codigo = self.dftab.loc[self.dftab['desc_produto'] == selecao_prod, 'cod_produto'].values[0]
        return codigo

def main(loja, tabela):
    placeholder = st.empty()
    placeholder2 = st.empty()
    produto=consulta_produto(tabela)
    dftab = pd.DataFrame(produto, columns = ['cod_produto', 'desc_produto'])

    while True: 
        num = st.session_state.num
        if placeholder2.button(f'***Enviar Pedido***', key=str(num)):
            placeholder2.empty()
            dfpedido = pd.DataFrame(st.session_state.data)
            dfpedido = dfpedido.drop_duplicates(subset=['cod_produto','nun_loja'], keep='last')
            if dfpedido.empty:
                st.markdown(f"\t<h6 style='text-align: center; color: with;'># O pedido não possui itens selecionados! #</h6>", unsafe_allow_html=True)
                break
            st.markdown(f"\n")
            data_atual = datetime.today()
            hoje = datetime.today().weekday()
            if len(dfpedido.index) != 0 and hoje in [0, 4, 5, 6]:
                    # Calcular a data da próxima sext-feira
                    proxima_sexta=dt_pedido_sexta(data_atual)
                    st.markdown(f"\t<h3 style='text-align: center; color: with;'># Pedido #</h3>", unsafe_allow_html=True)
                    st.markdown(f"\t<h5 style='text-align: center; color: with;'># Entrega prevista para {proxima_sexta} #</h5>", unsafe_allow_html=True)
                    df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                    st.dataframe(df_selecionado, hide_index=True)
                    loc = len(dfpedido.columns)
                    formato = "%d-%m-%Y"
                    proxima_sexta = datetime.strptime(proxima_sexta, formato)
                    dfpedido.insert(loc, 'dt_entrega', proxima_sexta)
                    insere_registros(dfpedido)
                    st.session_state.data = []
                    st.session_state.num = 0
                    break           
            elif len(dfpedido.index) != 0 and hoje in [1, 2, 3]:
                    # Calcular a data da próxima quarta-feira
                    proxima_quarta=dt_pedido_quarta(data_atual)
                    st.markdown(f"\t<h3 style='text-align: center; color: with;'># Pedido #</h3>", unsafe_allow_html=True)
                    st.markdown(f"\t<h6 style='text-align: center; color: with;'># Entrega prevista para - {proxima_quarta} #</h6>", unsafe_allow_html=True)    
                    df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                    st.dataframe(df_selecionado, hide_index=True)
                    loc = len(dfpedido.columns)
                    formato = "%d-%m-%Y"
                    proxima_quarta = datetime.strptime(proxima_quarta, formato)
                    dfpedido.insert(loc, 'dt_entrega', proxima_quarta)
                    insere_registros(dfpedido) 
                    st.session_state.data = []
                    st.session_state.num = 0
                    break             
        else:
           with placeholder.form(key=str(num)):
               dfpedido = pd.DataFrame(st.session_state.data)
               num_itens = len(dftab.index)
               num_pedido = len(dfpedido.index)
               if num >= num_itens and num_pedido == 0:
                   st.markdown(f"\t<h8 style='text-align: center; color: red;'># Nenhum produto selecionado, para continuar selecione um produto #</h8>", unsafe_allow_html=True)
                   dfpedido = dfpedido.drop_duplicates(subset=['cod_produto','nun_loja'], keep='last')
                   dfpedido = pd.DataFrame(st.session_state.data)              
                   st.session_state.num = 0
                   num = 0
               elif num >= num_itens and num_pedido > 0:
                   st.markdown(f"\t<h8 style='text-align: center; color: red;'># Não há mais produtos para seleção, para continuar precione ENVIAR PEDIDO #</h8>", unsafe_allow_html=True)
                   dfpedido = dfpedido.drop_duplicates(subset=['cod_produto','nun_loja'], keep='last')
                   dfpedido = pd.DataFrame(st.session_state.data)
                   num = 0           
               novo_produto = NovoPedido(page_id=num, tabela=tabela, dftab=dftab)
               submit_button = st.form_submit_button(label='Imagem do produto')
               if submit_button:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(' ')
                    with col2:
                        mostra_imagem(novo_produto.codigo)
                    with col3:
                        st.write(' ')
               vl_quantidade=st.text_input(label=f'****Quantidade****', value="")
               if st.form_submit_button('***Adicionar***'):
                    if vl_quantidade != "":
                        nun_loja = dftabloja.loc[dftabloja['LOJA'] == loja, 'TABELA'].values[0]
                        data_pedido=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.data.append({
                        'nun_loja': nun_loja,
                        'desc_loja': loja,
                        'dt_pedido': data_pedido,
                        'cod_produto': novo_produto.codigo,
                        'desc_produto': novo_produto.produto,
                        'quantidade': vl_quantidade
                        })
                        dfpedido = pd.DataFrame(st.session_state.data)
                        dfpedido = dfpedido.drop_duplicates(subset=['cod_produto','nun_loja'], keep='last')
                        st.markdown(f"\n")                     
                        df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                        st.markdown(f"\t<h5 style='text-align: center; color: with;'># Produto Selecionado #</h5>", unsafe_allow_html=True)
                        st.dataframe(df_selecionado, hide_index=True)
                        st.session_state.num += 1
                    elif vl_quantidade == "":
                        st.markdown(f"\t<h8 style='text-align: center; color: with;'># Necessário inserir uma quantidade #</h8>", unsafe_allow_html=True)
                        st.session_state.num += 1
                        dfpedido = pd.DataFrame(st.session_state.data)
                        if len(dfpedido.index) != 0:
                            dfpedido = dfpedido.drop_duplicates(subset='cod_produto').reset_index(drop=True)
                            df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                            st.dataframe(df_selecionado, hide_index=True)
               else:
                   st.stop()   

loja, tabela = selecionaloja()
if loja:
    main(loja, tabela)
    if st.button('Novo Pedido'):        
        loja = None
        page_id=0
        placeholder = st.empty()
        placeholder2 = st.empty()
        st.session_state.num = 0
        st.session_state.data = []        
        st.rerun()