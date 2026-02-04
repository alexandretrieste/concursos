import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Concurso SESC/SC - Preliminar",
    layout="wide"  # Layout amplo para ver melhor a tabela
)

# --- 2. CONTADOR DE ACESSOS (Selo Gratuito) ---
# Isso cria um contador visual que não zera quando o site reinicia
st.markdown("""
    <center>
    <img src="https://visitcount.itsvg.in/api?id=seunome_classificador&label=Acessos&color=0&icon=5&pretty=true" />
    </center>
    """, unsafe_allow_html=True)

st.title("🏆 Concurso SESC/SC - Preliminar")
st.markdown("Filtre, pesquise e baixe o resultado organizado por **Cargo** e **Cidade**.")

# --- 3. FUNÇÕES DE PROCESSAMENTO ---
def converter_para_float(valor):
    if pd.isna(valor): return 0.0
    try:
        return float(str(valor).replace(',', '.'))
    except:
        return 0.0

@st.cache_data # Isso faz o site ficar rápido (não recarrega o PDF toda hora)
def processar_pdf(uploaded_file):
    todas_linhas = []
    
    with pdfplumber.open(uploaded_file) as pdf:
        for i, pagina in enumerate(pdf.pages):
            tabela = pagina.extract_table()
            if tabela:
                if i == 0:
                    todas_linhas.extend(tabela)
                else:
                    if tabela[0] == todas_linhas[0]:
                        todas_linhas.extend(tabela[1:])
                    else:
                        todas_linhas.extend(tabela)

    if not todas_linhas:
        return None

    # Cria DataFrame e limpa cabeçalhos
    cabecalho = [str(c).replace('\n', ' ').strip().upper() for c in todas_linhas[0]]
    df = pd.DataFrame(todas_linhas[1:], columns=cabecalho)

    # Identificar colunas automaticamente (mesmo que o nome mude um pouco)
    col_nota = next((c for c in df.columns if 'NOTA' in c and 'OBJETIVA' in c), None)
    col_cargo = next((c for c in df.columns if 'CARGO' in c), None)
    col_cidade = next((c for c in df.columns if 'CIDADE' in c), None)
    col_nome = next((c for c in df.columns if 'NOME' in c), None)
    # A coluna de Inscrição geralmente é a segunda, mas vamos ignorar ela no final

    if not col_nota or not col_cargo or not col_cidade:
        return None

    # Converter notas e Classificar
    df[col_nota] = df[col_nota].apply(converter_para_float)
    df = df.sort_values(by=[col_cargo, col_cidade, col_nota], ascending=[True, True, False])
    
    # Criar Ranking (Reinicia a cada cidade/cargo)
    df.insert(0, 'Classificação', df.groupby([col_cargo, col_cidade]).cumcount() + 1)

    # --- FILTRO DE COLUNAS (O SEGREDO) ---
    # Selecionamos apenas as colunas que correspondem a A, B, D, E, K
    # A=Classificação, B=Nome, D=Cargo, E=Cidade, K=Nota
    colunas_finais = ['Classificação', col_nome, col_cargo, col_cidade, col_nota]
    
    # Filtra o DataFrame para ter somente essas colunas
    df_final = df[colunas_finais]
    
    # Renomeia para ficar bonito na tela
    df_final.columns = ['Posição', 'Nome do Candidato', 'Cargo', 'Cidade da Vaga', 'Nota Final']
    
    return df_final

# --- 4. INTERFACE ---
arquivo = st.file_uploader("📂 Arraste o PDF do resultado aqui", type="pdf")

if arquivo:
    with st.spinner('Lendo PDF e calculando posições...'):
        df_resultado = processar_pdf(arquivo)

    if df_resultado is not None:
        st.success("✅ Classificação gerada com sucesso!")
        
        # --- TABELA INTERATIVA (COM PESQUISA) ---
        # O st.dataframe permite ordenar clicar nas colunas e tem lupa de pesquisa (canto superior direito da tabela)
        st.dataframe(df_resultado, use_container_width=True, hide_index=True)

        # Botão de Download
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_resultado.to_excel(writer, index=False)
            
        st.download_button(
            label="📥 Baixar Planilha Excel (Limpa)",
            data=buffer.getvalue(),
            file_name="resultado_classificado.xlsx",
            mime="application/vnd.ms-excel",
            type="primary"
        )
    else:
        st.error("Não foi possível ler a tabela do PDF. Verifique se o formato está correto.")