import streamlit as st
import pandas as pd

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Concurso SES/SC - Preliminar",
    layout="wide",
    page_icon="🏆"
)

# --- 2. CONTADOR DE VISITAS (Selo) ---
st.markdown("""
    <center>
    <img src="https://visitcount.itsvg.in/api?id=resultado_concurso_oficial_v2&label=Visualizacoes&color=0&icon=5&pretty=true" />
    </center>
    """, unsafe_allow_html=True)

st.title("🏆 Concurso SES/SC - Preliminar")
st.markdown("Consulte a classificação oficial abaixo.")

# --- 3. CARREGAR DADOS (Estrito: Colunas A, B, D, E, K) ---
@st.cache_data
def carregar_dados():
    arquivo = 'resultado_final_pdf.xlsx'
    try:
        # usecols="A,B,D,E,K" -> Lê EXATAMENTE as colunas que você pediu
        # A=Classificação, B=Nome, D=Cargo, E=Cidade, K=Nota
        df = pd.read_excel(arquivo, usecols="A,B,D,E,K")
        
        # Renomeia para ficar bonito na tela (na ordem que elas entram)
        df.columns = ['Classificação', 'Nome do Candidato', 'Cargo', 'Cidade da Vaga', 'Nota Final']
        
        return df
    except FileNotFoundError:
        st.error("❌ Erro: O arquivo 'resultado_final_pdf.xlsx' não está na pasta.")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao ler o Excel: {e}")
        return None

df = carregar_dados()

if df is not None:
    # --- 4. BARRA DE PESQUISA INTELIGENTE ---
    with st.container():
        # Cria duas colunas para alinhar a busca
        col_busca, col_info = st.columns([4, 1])
        
        with col_busca:
            texto_busca = st.text_input("🔍 Pesquisar por Nome, Cargo ou Cidade:", placeholder="Ex: Motorista")
        
        with col_info:
            st.write("") # Espaçamento
            st.write(f"**Total:** {len(df)} registros")

    # --- 5. FILTRAGEM ---
    if texto_busca:
        # Procura o texto em qualquer coluna da tabela
        filtro = df.astype(str).apply(lambda x: x.str.contains(texto_busca, case=False)).any(axis=1)
        df_exibicao = df[filtro]
    else:
        df_exibicao = df

    # --- 6. TABELA FINAL ---
    st.dataframe(
        df_exibicao,
        use_container_width=True, # Ocupa a largura total da tela
        hide_index=True,          # Esconde o índice numérico lateral (0,1,2...)
        height=600                # Altura fixa para barra de rolagem
    )

else:

    st.warning("Dica: Certifique-se de que o arquivo 'resultado_final_pdf.xlsx' foi gerado pelo script anterior e está nesta mesma pasta.")

