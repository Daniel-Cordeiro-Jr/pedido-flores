import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import sqlalchemy as sa
import datetime as dt
import psycopg2 as pg
import datetime as dt
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

def mostra_imagem(codigo):
    # Diretório onde as imagens estão armazenadas
    diretorio_imagens = "imagem"
    # Formata a imagem
    st.markdown("""<style>img {border: 6px solid green;}</style>""", unsafe_allow_html=True)
    # Abre a imagem selecionada
    imagem = Image.open(os.path.join(diretorio_imagens, codigo + ".jpeg"))
    # Mostra a imagem no Streamlit
    st.image(imagem)

def dt_pedido():
    data_atual = dt.datetime.now()
    # Dia da semana da próxima quarta-feira (2)
    proxima_quarta = 2
    # Dia da semana atual
    hoje = data_atual.weekday()
    # Calcular quantos dias até a próxima quarta-feira
    dias_ate_quarta = (proxima_quarta - hoje + 7) % 7
    # Se hoje já é quarta-feira, definir para a quarta-feira da próxima semana
    if dias_ate_quarta == 0:
        dias_ate_quarta += 7
    # Calcular a data da quarta-feira da próxima semana
    data_proxima_quarta = dt.datetime.today() + dt.timedelta(days=dias_ate_quarta)
    # Formatar a data no formato 'dia/mês/ano'
    data_formatada = data_proxima_quarta.strftime('%d-%m-%Y')
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
        index=num+1
        if placeholder2.button(f'***Enviar Pedido***', key=str(index)):
            placeholder2.empty()
            dfpedido = pd.DataFrame(st.session_state.data)
            dfpedido = dfpedido.drop_duplicates(subset='cod_produto').reset_index(drop=True)
            st.markdown(f"\n")
            data_atual = dt.date.today().weekday()
            if data_atual in [0, 4, 5, 6]:
                dias_ate_sexta = ((4 - data_atual) % 7) + 7
                entrega=dt.date.today() + dt.timedelta(days=dias_ate_sexta)
                st.markdown(f"\t<h3 style='text-align: center; color: with;'># Pedido #</h3>", unsafe_allow_html=True)
                st.markdown(f"\t<h5 style='text-align: center; color: with;'># Data de entrega prevista para {entrega} #</h5>", unsafe_allow_html=True)
                df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                st.dataframe(df_selecionado, hide_index=True)
                break
            
            elif data_atual > 0 and data_atual <= 3:
                # Calcular a data da próxima quarta-feira
                proxima_quarta=dt_pedido()
                st.markdown(f"\t<h3 style='text-align: center; color: with;'># Pedido #</h3>", unsafe_allow_html=True)
                st.markdown(f"\t<h6 style='text-align: center; color: with;'># Entrega prevista para - {proxima_quarta} #</h6>", unsafe_allow_html=True)
                df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                st.dataframe(df_selecionado, hide_index=True)
                break
            
            exporta_pedido(dfpedido) 
            st.session_state.num = 1
            st.session_state.data = []
        else:
           with placeholder.form(key=str(num)):
               num_linhas = len(dftab.index)
               if num >= num_linhas:
                   num = 0
                   st.session_state.num = 0
               novo_produto = NovoPedido(page_id=num)
               submit_button = st.form_submit_button(label='Imagem')
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
                        st.markdown(f"\t<h5 style='text-align: center; color: with;'># Itens Selecionados #</h5>", unsafe_allow_html=True)
                        df_selecionado = dfpedido[['desc_produto', 'quantidade']]
                        st.dataframe(df_selecionado, hide_index=True)
                        st.session_state.num += 1
                    elif vl_quantidade == "":
                        st.markdown(f"\t<h5 style='text-align: center; color: red;'># Item sem quantidade #</h5>", unsafe_allow_html=True)
                        st.session_state.num += 1
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
        placeholder = st.empty()
        placeholder2 = st.empty()
        st.session_state.num = ""
        st.stop()


