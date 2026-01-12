import streamlit as st
import pandas as pd

# === CONFIGURAÇÃO DA PÁGINA ===
st.set_page_config(
    page_title="Painel de Concorrência - SES/SC 2026",
    page_icon="📊",
    layout="wide"
)

# === CARREGAMENTO DE DADOS ===
@st.cache_data
def carregar_dados():
    arquivo = "Relatorio_Final_Concorrencia.xlsx"
    try:
        df = pd.read_excel(arquivo)
        return df
    except FileNotFoundError:
        return None

df = carregar_dados()

# === TÍTULO E CABEÇALHO ===
st.title("📊 Painel de Concorrência do Concurso")
st.markdown("Visualize facilmente a relação **Candidato/Vaga** por Unidade e Cidade.")

if df is not None:
    # === BARRA LATERAL (FILTROS) ===
    st.sidebar.header("Filtros")
    
    # Filtro 1: Unidade
    todas_unidades = df["Unidade"].unique()
    unidade_selecionada = st.sidebar.multiselect(
        "Selecione a Unidade:",
        options=todas_unidades,
        default=todas_unidades
    )
    
    # Filtro 2: Cidade (baseado na unidade selecionada)
    df_filtrado_unidade = df[df["Unidade"].isin(unidade_selecionada)]
    todas_cidades = df_filtrado_unidade["Cidade"].unique()
    
    cidade_selecionada = st.sidebar.multiselect(
        "Selecione a Cidade:",
        options=todas_cidades,
        default=todas_cidades
    )
    
    # Aplica filtros
    df_final = df_filtrado_unidade[df_filtrado_unidade["Cidade"].isin(cidade_selecionada)]

    # === MÉTRICAS (KPIs) ===
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Vagas (Filtro)", int(df_final["Vagas (Ampla)"].sum()))
    col2.metric("Total de Inscritos (Filtro)", int(df_final["Total Inscritos"].sum()))
    
    # Calcula média de concorrência segura (evita div por 0)
    if not df_final.empty:
        media_conc = df_final["Total Inscritos"].sum() / df_final["Vagas (Ampla)"].sum() if df_final["Vagas (Ampla)"].sum() > 0 else 0
        col3.metric("Concorrência Média Geral", f"{media_conc:.2f} c/v")

    # === TABELA INTERATIVA ===
    st.divider()
    st.subheader("Detalhes dos Cargos")
    
    # Formatação visual (Dataframe com highlight na concorrência)
    st.dataframe(
        df_final.style.background_gradient(subset=["Concorrencia"], cmap="Reds"),
        use_container_width=True,
        column_config={
            "Concorrencia": st.column_config.NumberColumn(
                "Concorrência (Cand/Vaga)",
                format="%.2f"
            ),
            "Vagas (Ampla)": st.column_config.NumberColumn(
                "Vagas",
                format="%d"
            )
        },
        height=600
    )

    # === RODAPÉ (Inserido Aqui) ===
    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns([1, 4, 1])
    with col_f2:
        st.markdown(
            """
            <div style="text-align: center; color: #666;">
                <p style="font-size: 14px; margin-bottom: 5px;">
                    🚀 <strong>Painel de Concorrência</strong> | Desenvolvido para fins informativos - Por Alexandre Trieste
                </p>
                <p style="font-size: 12px; color: #888;">
                    Os dados foram processados automaticamente a partir dos arquivos PDF oficiais.<br>
                    Este projeto não possui vínculo com a banca organizadora.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.error("Erro: O arquivo 'Relatorio_Final_Concorrencia.xlsx' não foi encontrado na pasta.")

    st.info("Certifique-se de ter rodado o script de geração antes de abrir o site.")
