import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

# ---------------------------------------------------------
# CONFIGURAÇÃO VISUAL - IDENTITY AMIRA (DARK / NEON TECH)
# ---------------------------------------------------------
st.set_page_config(
    page_title="AMIRA - Controle de Pesagem",
    page_icon="⚡",
    layout="wide"
)

# Estilização CSS com a paleta da AMIRA
st.markdown("""
    <style>
    /* Fundo da aplicação */
    .stApp {
        background-color: #0b0c12;
        color: #e0e6ed;
    }
    
    /* Estilização da Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #131521 !important;
        border-right: 1px solid #8a2be2;
    }

    /* Estilização dos Cards de Métricas */
    div[data-testid="stMetricValue"] {
        color: #00d2ff !important;
        font-weight: 700;
        font-size: 2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #a0aab8 !important;
        font-weight: 600;
    }
    .stMetric {
        background: linear-gradient(145deg, #131521, #1a1d2e);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
        border-left: 4px solid #00a2ff;
        border-right: 1px solid #8a2be2;
    }

    /* Botões Futuristas com Gradiente AMIRA */
    .stButton>button, div[data-testid="stDownloadButton"]>button {
        background: linear-gradient(90deg, #00a2ff 0%, #8a2be2 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 0 12px rgba(0, 162, 255, 0.4);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover, div[data-testid="stDownloadButton"]>button:hover {
        box-shadow: 0 0 22px rgba(138, 43, 226, 0.8) !important;
        transform: translateY(-2px);
    }

    /* Selectbox e Rótulos */
    .stSelectbox label {
        color: #00a2ff !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    div[data-baseweb="select"] {
        background-color: #131521 !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: 1px solid #8a2be2;
    }
    
    /* Título e Subtítulos */
    h1 {
        background: linear-gradient(90deg, #ffffff 30%, #00a2ff 70%, #8a2be2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    h2, h3, h4 {
        color: #ffffff !important;
    }
    
    /* Tabelas em modo Dark */
    div[data-testid="stDataFrame"] {
        background-color: #131521;
        border-radius: 10px;
        border: 1px solid #292d3e;
    }
    </style>
""", unsafe_allow_html=True)

URL_SCRIPT = "https://script.google.com/macros/s/AKfycbz55nUlT6dBdbIJ15pWoNN4yNzLv0tC4XBxHkojHJTz_CB_HbsN6JTMUb_mw5338GgjMA/exec"

# ---------------------------------------------------------
# LEITURA DOS DADOS DAS ABAS
# ---------------------------------------------------------
@st.cache_data(ttl=2)
def carregar_dados_todas_abas():
    try:
        res = requests.get(URL_SCRIPT)
        dados_json = res.json()
        
        dict_dfs = {}
        for nome_aba, conteudo in dados_json.items():
            if len(conteudo) > 1:
                df = pd.DataFrame(conteudo[1:], columns=conteudo[0])
                df["Peso"] = pd.to_numeric(df["Peso"], errors='coerce')
                dict_dfs[nome_aba] = df
        return dict_dfs
    except Exception as e:
        return {}

# ---------------------------------------------------------
# LOGO NA BARRA LATERAL (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_column_width=True)
    elif os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    st.markdown("### **AMIRA System**")
    st.caption("Tecnologia e Inteligência em Pesagem")
    st.markdown("---")

# ---------------------------------------------------------
# CABEÇALHO DO APLICATIVO COM A LOGO
# ---------------------------------------------------------
col_logo, col_title, col_btn = st.columns([1, 3, 1])

with col_logo:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=110)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=110)

with col_title:
    st.title("AMIRA — Gestão & Pesagem")
    st.caption("Monitoramento e análise preditiva de produção em tempo real")

with col_btn:
    st.write("")
    if st.button("🔄 Sincronizar"):
        st.cache_data.clear()
        st.rerun()

dados_abas = carregar_dados_todas_abas()

if not dados_abas:
    st.warning("⚠️ Conectando ao Banco de Dados AMIRA... Aguarde ou verifique se existem novos registros na balança.")
    st.stop()

# ---------------------------------------------------------
# NAVEGAÇÃO DE ABAS POR DATA
# ---------------------------------------------------------
st.markdown("---")
lista_datas = list(dados_abas.keys())
data_selecionada = st.selectbox("📅 Selecionar Dia de Produção (Aba Ativa):", options=lista_datas, index=0)

df_dia = dados_abas[data_selecionada]

# ---------------------------------------------------------
# CARDS DE MÉTRICAS DO DIA
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

total_caixas = len(df_dia)
media_peso = df_dia["Peso"].mean() if not df_dia.empty else 0
peso_total_dia = df_dia["Peso"].sum() if not df_dia.empty else 0

with col1:
    st.metric(label="📦 Caixas Pesadas", value=f"{total_caixas}")

with col2:
    st.metric(label="⚖️ Média de Peso Diária", value=f"{media_peso:.2f} kg")

with col3:
    st.metric(label="📊 Volume Total Processado", value=f"{peso_total_dia:.2f} kg")

# ---------------------------------------------------------
# VISUALIZAÇÃO DOS PESOS DO DIA (TABELA E GRÁFICO)
# ---------------------------------------------------------
st.markdown("---")
st.subheader(f"📋 Registros Operacionais — Data: {data_selecionada}")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.write("#### Tabela de Registros")
    st.dataframe(df_dia, use_container_width=True)

with col_right:
    st.write("#### Variação do Peso em Tempo Real")
    if not df_dia.empty:
        fig_linha = px.line(
            df_dia, 
            x="Hora", 
            y="Peso", 
            markers=True,
            title="Oscilação por Unidade Pesada",
            template="plotly_dark"
        )
        fig_linha.update_traces(line_color='#00a2ff', marker=dict(size=8, color='#8a2be2'))
        fig_linha.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_linha, use_container_width=True)

# ---------------------------------------------------------
# ANÁLISE MENSAL DE 35 DIAS
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📈 Inteligência Analítica dos Últimos 35 Dias")

resumo_dias = []
todos_pesos_mes = []

for data_nome, df_temp in dados_abas.items():
    if not df_temp.empty:
        cnt = len(df_temp)
        med = df_temp["Peso"].mean()
        resumo_dias.append({"Data": data_nome, "Média Peso (kg)": med, "Qtd Caixas": cnt})
        todos_pesos_mes.extend(df_temp["Peso"].dropna().tolist())

df_resumo_mes = pd.DataFrame(resumo_dias)

col_mes_1, col_mes_2 = st.columns(2)

with col_mes_1:
    st.write("#### Peso Médio Comparativo por Dia")
    if not df_resumo_mes.empty:
        fig_bar = px.bar(
            df_resumo_mes, 
            x="Data", 
            y="Média Peso (kg)", 
            text_auto='.2f',
            template="plotly_dark",
            color="Média Peso (kg)",
            color_continuous_scale=["#00a2ff", "#8a2be2"]
        )
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

with col_mes_2:
    st.write("#### Recorrência dos Pesos no Mês")
    if todos_pesos_mes:
        df_pesos_frequentes = pd.DataFrame({"Peso": todos_pesos_mes})
        df_pesos_frequentes["Peso_Arredondado"] = df_pesos_frequentes["Peso"].round(2).astype(str) + " kg"
        contagem_pesos = df_pesos_frequentes["Peso_Arredondado"].value_counts().reset_index()
        contagem_pesos.columns = ["Peso", "Quantidade"]

        fig_pizza = px.pie(
            contagem_pesos, 
            names="Peso", 
            values="Quantidade", 
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=['#00a2ff', '#8a2be2', '#3a86ff', '#8338ec', '#ff007f']
        )
        fig_pizza.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pizza, use_container_width=True)

# ---------------------------------------------------------
# EXPORTAÇÃO DE DADOS
# ---------------------------------------------------------
st.markdown("---")
csv_data = df_dia.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label=f"📥 Exportar Planilha de {data_selecionada} (Excel / CSV)",
    data=csv_data,
    file_name=f"AMIRA_Pesagens_{data_selecionada}.csv",
    mime="text/csv"
)
