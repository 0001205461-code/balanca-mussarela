import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

# ---------------------------------------------------------
# CONFIGURAÇÃO VISUAL - IDENTITY AMIRA (DARK / NEON TECH)
# ---------------------------------------------------------
st.set_page_config(
    page_title="AMIRA",
    page_icon="⚡",
    layout="wide"
)

# Estilização CSS personalizada AMIRA
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

    /* Abas / Menu Superior (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #131521;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #8a2be2;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #0b0c12;
        border-radius: 8px;
        color: #a0aab8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00a2ff 0%, #8a2be2 100%) !important;
        color: #ffffff !important;
        font-weight: bold;
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
    
    /* Título */
    h1 {
        background: linear-gradient(90deg, #ffffff 30%, #00a2ff 70%, #8a2be2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem !important;
        margin-bottom: 0px;
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
URL_LOGO = "https://i.postimg.cc/85y98G6p/amira-logo.jpg"

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
                if "Peso" in df.columns:
                    df["Peso"] = pd.to_numeric(df["Peso"], errors='coerce')
                dict_dfs[nome_aba] = df
        return dict_dfs
    except Exception as e:
        return {}

# ---------------------------------------------------------
# BARRA LATERAL (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)
    elif os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.image(URL_LOGO, use_container_width=True)
        
    st.markdown("### **AMIRA System**")
    st.caption("Tecnologia e Inteligência")
    st.markdown("---")

# ---------------------------------------------------------
# CABEÇALHO DA PÁGINA
# ---------------------------------------------------------
col_title, col_btn = st.columns([4, 1])

with col_title:
    st.title("AMIRA")

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
# MENU POR NAVEGAÇÃO DE ABAS
# ---------------------------------------------------------
tab_registros, tab_graficos, tab_nova_aba = st.tabs(["📋 Registros & Dados", "📊 Gráficos & Análises", "➕ Nova Aba"])

# ---------------------------------------------------------
# ABA 1: REGISTROS & DADOS
# ---------------------------------------------------------
with tab_registros:
    st.markdown("<br>", unsafe_allow_html=True)
    lista_datas = list(dados_abas.keys())
    data_selecionada = st.selectbox("📅 Selecionar Dia de Produção:", options=lista_datas, index=0)

    df_dia = dados_abas[data_selecionada]

    # Cards de Métricas
    col1, col2, col3 = st.columns(3)
    total_caixas = len(df_dia)
    media_peso = df_dia["Peso"].mean() if ("Peso" in df_dia.columns and not df_dia.empty) else 0
    peso_total_dia = df_dia["Peso"].sum() if ("Peso" in df_dia.columns and not df_dia.empty) else 0

    with col1:
        st.metric(label="📦 Caixas Pesadas", value=f"{total_caixas}")
    with col2:
        st.metric(label="⚖️ Média de Peso Diária", value=f"{media_peso:.2f} kg")
    with col3:
        st.metric(label="📊 Volume Total Processado", value=f"{peso_total_dia:.2f} kg")

    st.markdown("---")
    st.write(f"### Tabela de Registros — Data: **{data_selecionada}**")
    st.dataframe(df_dia, use_container_width=True, height=400)

    # Botão de exportação
    csv_data = df_dia.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label=f"📥 Exportar Planilha ({data_selecionada})",
        data=csv_data,
        file_name=f"AMIRA_{data_selecionada}.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# ABA 2: GRÁFICOS & ANÁLISES
# ---------------------------------------------------------
with tab_graficos:
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("### 📈 Visualizações Gráficas e Análise de Produção")
    
    # Gráfico 1: Linha de variação do dia selecionado
    lista_datas = list(dados_abas.keys())
    data_grafico = st.selectbox("📊 Selecionar dia para ver o gráfico de oscilação:", options=lista_datas, index=0)
    df_graf = dados_abas[data_grafico]

    if not df_graf.empty and "Peso" in df_graf.columns and "Hora" in df_graf.columns:
        fig_linha = px.line(
            df_graf, 
            x="Hora", 
            y="Peso", 
            markers=True,
            title=f"Oscilação por Unidade Pesada ({data_grafico})",
            template="plotly_dark"
        )
        fig_linha.update_traces(line_color='#00a2ff', marker=dict(size=8, color='#8a2be2'))
        fig_linha.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_linha, use_container_width=True)

    st.markdown("---")
    
    # Gráficos Comparativos Gerais (Histórico)
    st.write("### 📊 Análise Comparativa Entre os Dias")
    resumo_dias = []
    todos_pesos_mes = []

    for data_nome, df_temp in dados_abas.items():
        if not df_temp.empty and "Peso" in df_temp.columns:
            cnt = len(df_temp)
            med = df_temp["Peso"].mean()
            resumo_dias.append({"Data": data_nome, "Média Peso (kg)": med, "Qtd Caixas": cnt})
            todos_pesos_mes.extend(df_temp["Peso"].dropna().tolist())

    df_resumo_mes = pd.DataFrame(resumo_dias)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.write("#### Média de Peso por Dia")
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

    with col_g2:
        st.write("#### Distribuição/Frequência dos Pesos")
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
# ABA 3: NOVA ABA / CRIAR DIA
# ---------------------------------------------------------
with tab_nova_aba:
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("### ➕ Criar Nova Aba / Novo Dia de Produção")
    
    with st.form("form_nova_aba"):
        nova_data_nome = st.text_input("Digite a data ou nome para a nova aba (Ex: 18-08-2026):")
        btn_criar = st.form_submit_button("Criar Nova Aba na Planilha")
        
        if btn_criar:
            if nova_data_nome.strip():
                try:
                    payload = {"action": "criar_aba", "nome_aba": nova_data_nome.strip()}
                    res = requests.post(URL_SCRIPT, json=payload)
                    st.success(f"✅ Comando enviado! A aba '{nova_data_nome}' foi criada com sucesso.")
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"Erro ao tentar criar a aba: {e}")
            else:
                st.warning("⚠️ Informe um nome de aba válido.")
