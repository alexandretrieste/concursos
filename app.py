import streamlit as st
import pandas as pd

# --- 1. CONFIGURAÇÃO DA PÁGINA (TÍTULO DA ABA) ---
st.set_page_config(
    page_title="Concurso SESC/SC - Preliminar",
    layout="wide",
    page_icon="🏆"
)

# --- 2. CONTADOR DE ACESSOS ---
# Usando um contador estável (estilo "Flat Blue")
st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://komarev.com/ghpvc/?username=resultado_concurso_sesc_sc_preliminar&label=VISUALIZACOES&color=blue&style=flat" alt="Contador de Visitas" />
    </div>
    """, unsafe_allow_html=True)

# --- 3. TÍTULO E SUBTÍTULO (IGUAL AO PRINT) ---
st.title("🏆 Concurso SESC/SC - Preliminar")
st.markdown("Filtre, pesquise e baixe o resultado organizado por **Cargo** e **Cidade**.")

# --- 4. CARREGAR DADOS (Colunas A, B, D, E, K) ---
@st.cache_data
def carregar_dados():
    arquivo = 'resultado_final_pdf.xlsx'
    try:
        # Lê estritamente as colunas A, B, D, E, K
        df = pd.read_excel(arquivo, usecols="A,B,D,E,K")
        
        # Renomeia para exibição
        df.columns = ['Classificação', 'Nome do Candidato', 'Cargo', 'Cidade da Vaga', 'Nota Final']
        
        return df
    except FileNotFoundError:
        st.error("❌ O arquivo 'resultado_final_pdf.xlsx' não foi encontrado.")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao ler arquivo: {e}")
        return None

df = carregar_dados()

if df is not None:
    # --- 5. BARRA DE PESQUISA ---
    # Container para alinhar a busca e o total
    with st.container():
        col_busca, col_info = st.columns([4, 1])
        
        with col_busca:
            texto_busca = st.text_input("🔍 Pesquisar por Nome, Cargo ou Cidade:", placeholder="Ex: Motorista")
        
        with col_info:
            st.write("") # Espaço para alinhar verticalmente
            st.write(f"**Total:** {len(df)} registros")

    # --- 6. FILTRO E TABELA ---
    if texto_busca:
        # Filtra em qualquer coluna
        filtro = df.astype(str).apply(lambda x: x.str.contains(texto_busca, case=False)).any(axis=1)
        df_exibicao = df[filtro]
    else:
        df_exibicao = df

    # Exibe a tabela ocupando a largura total
    st.dataframe(
        df_exibicao,
        use_container_width=True,
        hide_index=True,
        height=600
    )

else:
    st.warning("O arquivo de dados não está na pasta. Rode o script de processamento primeiro.")