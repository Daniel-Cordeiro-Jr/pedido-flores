#Versão completa

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


# Carregar o arquivo style.css
with open ("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega a imagem do logo
st.image('logo.jpeg', use_column_width = True)

# Carrega a tabela com Mercadorias e Quantidades a serem trabalhadas
dftab = pd.read_excel(f'mercadoria.xlsx')

dftab.index = pd.RangeIndex(start=1, stop=len(dftab) + 1)

# Formata os campos da tabela de dados
dftab = dftab.astype({'cod_produto': 'str', 'desc_produto': 'str'})

# Carrega a tabela Loja
dftabloja= pd.read_excel(f'loja.xlsx')

# Formata os campos da tabela loja
dftabloja = dftabloja.astype({'numero': 'str', 'loja': 'str'})

def get_quantidades(codigo):
    # Selecionar as colunas de quantidade e converter para uma lista
    if codigo:
        quantidades = None
        quantidades = dftab.loc[dftab['cod_produto'] == codigo, ['minimo','qtd2','qtd3','qtd4']].values[0]
        return quantidades

def config_db():
    # Abre o arquivo em modo de leitura ('r')
    arquivo = open('config_db.txt', 'r')
    # Lê o conteúdo do arquivo
    conteudo = arquivo.read()
    # Fecha o arquivo
    arquivo.close()
    return conteudo

def exporta_pedido(dfpedido):
    # Cria uma conexão com o banco de dados PostgreSQL
    #strdb = config_db()
    engine = sa.create_engine('postgresql://giygdfhjyrwsdq:f4d9c1d659860884bcb677f89ad33155a3e68e5fac95eb1b3054fc2308ef5389@ec2-18-213-255-35.compute-1.amazonaws.com:5432/d4vnafvevfvp4s')
    #engine = sa.create_engine(strdb)
    # Faz a inserção dos dados no banco de dados PostgreSQL
    dfpedido.to_sql('tb_pedidos', con=engine, if_exists='append', index=False)
    # Exclui a seleção antiga.
    st.session_state.data = []
    st.session_state.num = 0

def mostra_imagem(codigo):
    # Diretório onde as imagens estão armazenadas
    diretorio_imagens = "imagem"
    # Abre a imagem selecionada
    imagem = Image.open(os.path.join(diretorio_imagens, codigo + ".jpeg"))
    # Formatando imagem
    st.markdown("""<style>img {border: 4px solid green;}</style>""", unsafe_allow_html=True)
    # Mostra a imagem no Streamlit
    st.image(imagem)

def dt_pedido_quarta(data_atual):
    # Calcular o número de dias até a próxima sexta-feira
    dias_ate_quarta = (2 - data_atual.weekday() + 7) % 7
    # Calcular a data da próxima sexta-feira
    proxima_quarta = data_atual + dt.timedelta(days=dias_ate_quarta + 7)
    # Formatar o objeto datetime para o formato desejado
    data_formatada = proxima_quarta.strftime('%d-%m-%Y')
    return data_formatada

def dt_pedido_sexta(data_atual):
    # Calcular o número de dias até a próxima sexta-feira
    dias_ate_sexta = (4 - data_atual.weekday() + 7) % 7
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
    def __init__(self, page_id):
        self.produto = self.selecionaproduto(page_id)
        self.codigo = self.retorna_codigo(self.produto)

    def selecionaproduto(self, page_id):
        produto = st.selectbox(f'****Produto:****', dftab['desc_produto'],
                               index=page_id,
                               placeholder="Selecione o produto...")
        return produto
    def retorna_codigo(self, selecao_prod):
        codigo = dftab.loc[dftab['desc_produto'] == selecao_prod, 'cod_produto'].values[0]
        return codigo
def main(loja):
    placeholder = st.empty()
    placeholder2 = st.empty()
    while True: 
        num = st.session_state.num
        if placeholder2.button(f'***Enviar Pedido***', key=str(num)):
            placeholder2.empty()
            dfpedido = pd.DataFrame(st.session_state.data)
            dfpedido = dfpedido.drop_duplicates(subset='cod_produto').reset_index(drop=True)
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
                    exporta_pedido(dfpedido)
                    break           
            elif len(dfpedido.index) != 0 and hoje in [1, 2, 3]:
                    # Calcular a data da próxima quarta-feira
                    proxima_quarta=dt_pedido_quarta(data_atual)
                    st.markdown(f"\t<h3 style='text-align: center; color: with;'># Pedido #</h3>", unsafe_allow_html=True)
                    st.markdown(f"\t<h6 style='text-align: center; color: with;'># Entrega prevista para - {proxima_quarta} #</h6>", unsafe_allow_html=True)    
                    df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                    st.dataframe(df_selecionado, hide_index=True)
                    exporta_pedido(dfpedido) 
                    break
              
        else:
           with placeholder.form(key=str(num)):
               dfpedido = pd.DataFrame(st.session_state.data)
               num_itens = len(dftab.index)
               num_pedido = len(dfpedido.index)
               if num >= num_itens and num_pedido == 0:
                   st.markdown(f"\t<h8 style='text-align: center; color: black;'># Nenhum produto selecionado, para continuar selecione um produto #</h8>", unsafe_allow_html=True)              
                   dfpedido = dfpedido.drop_duplicates(subset='cod_produto').reset_index(drop=True)
                   dfpedido = pd.DataFrame(st.session_state.data)              
                   st.session_state.num = 0
                   num = 0
               elif num >= num_itens and num_pedido > 0:
                   st.markdown(f"\t<h8 style='text-align: center; color: black;'># Não há mais produtos para seleção, para continuar precione ENVIAR PEDIDO #</h8>", unsafe_allow_html=True)              
                   dfpedido = dfpedido.drop_duplicates(subset='cod_produto').reset_index(drop=True)
                   dfpedido = pd.DataFrame(st.session_state.data)
                   st.session_state.num = 0
                   num = 0                   

               novo_produto = NovoPedido(page_id=num)
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
                        nun_loja = dftabloja.loc[dftabloja['loja'] == loja, 'numero'].values[0]
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
                        dfpedido = dfpedido.drop_duplicates(subset='cod_produto').reset_index(drop=True)
                        st.markdown(f"\n")                     
                        df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                        st.markdown(f"\t<h5 style='text-align: center; color: black;'># Produto Selecionado #</h5>", unsafe_allow_html=True)
                        st.dataframe(df_selecionado, hide_index=True)
                        st.session_state.num += 1
                    elif vl_quantidade == "":
                        st.markdown(f"\t<h8 style='text-align: center; color: black;'># Necessário inserir a quantidade #</h8>", unsafe_allow_html=True)
                        st.session_state.num += 1
                        dfpedido = pd.DataFrame(st.session_state.data)
                        if len(dfpedido.index) != 0:
                            df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                            st.dataframe(df_selecionado, hide_index=True)
               else:
                   st.stop()
                   
def selecionaloja():
#Selecionar a Loja 
    mensagem = "Selecione a Loja..."
    selected_option = st.selectbox(f'****Loja:****', dftabloja['loja'],
                               index = None, 
                               placeholder=mensagem)
    return selected_option
loja = selecionaloja()
if loja:
    main(loja)
    if st.button('Novo Pedido'):        
        loja = None
        page_id=0
        placeholder = st.empty()
        placeholder2 = st.empty()
        st.session_state.num = 0
        st.session_state.data = []        
        st.rerun()


