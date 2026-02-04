import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Concurso SESC/SC - Preliminar",
    layout="wide",
    page_icon="🏆"
)

st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://komarev.com/ghpvc/?username=resultado-concurso-sesc-sc-preliminar&label=VISUALIZACOES&color=blue&style=flat" alt="Contador de Visitas" />
    </div>
    """, unsafe_allow_html=True)

st.title("🏆 Concurso SESC/SC - Preliminar")
st.markdown("Filtre, pesquise e baixe o resultado organizado por **Cargo** e **Cidade**.")

@st.cache_data
def carregar_dados():
    arquivo = 'resultado_final_pdf.xlsx'
    try:
        
        df = pd.read_excel(arquivo, usecols="A,B,D,E,K")
        
        
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
   
    with st.container():
        col_busca, col_info = st.columns([4, 1])
        
        with col_busca:
            texto_busca = st.text_input("🔍 Pesquisar por Nome, Cargo ou Cidade:", placeholder="Ex: Motorista")
        
        with col_info:
            st.write("") 
            st.write(f"**Total:** {len(df)} registros")

    
    if texto_busca:
        filtro = df.astype(str).apply(lambda x: x.str.contains(texto_busca, case=False)).any(axis=1)
        df_exibicao = df[filtro]
    else:
        df_exibicao = df

    st.dataframe(
        df_exibicao,
        use_container_width=True,
        hide_index=True,
        height=600
    )

else:
    st.warning("O arquivo de dados não está na pasta.")