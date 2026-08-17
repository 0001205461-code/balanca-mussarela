import io
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# =========================================================
# AMIRA — PAINEL DE MONITORAMENTO DA BALANÇA
# =========================================================

st.set_page_config(
    page_title="AMIRA | Monitoramento de Produção",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------
URL_SCRIPT = "https://script.google.com/macros/s/AKfycby-Hb_1HMUpeWLlfldmIDXjP-OgiwXCTpXxsixygnkRISFGlawIuDlA0SRdXQjegnENyA/exec"
TZ = "America/Sao_Paulo"

# ---------------------------------------------------------
# CSS — VISUAL AMIRA
# ---------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@600;700;800&display=swap');

:root {
    --bg: #05070d;
    --panel: #0b0f1a;
    --panel2: #0f1422;
    --line: rgba(85, 139, 255, .24);
    --blue: #2f80ff;
    --cyan: #00d2ff;
    --purple: #8a35ff;
    --text: #f4f7ff;
    --muted: #8f9bb2;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 70% 15%, rgba(54, 83, 180, .12), transparent 28%),
        radial-gradient(circle at 95% 75%, rgba(138, 53, 255, .10), transparent 30%),
        #05070d;
    color: var(--text);
}

.block-container {
    padding: 1.5rem 2rem 2rem 2rem;
    max-width: 1700px;
}

section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 50% 15%, rgba(50, 117, 255, .10), transparent 25%),
        linear-gradient(180deg, #070a12 0%, #080b14 100%) !important;
    border-right: 1px solid rgba(76, 122, 255, .18);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}

.sidebar-logo {
    width: 100%;
    max-height: 185px;
    object-fit: contain;
    border-radius: 16px;
    filter: drop-shadow(0 0 18px rgba(45, 126, 255, .16));
}

.brand-small {
    text-align: center;
    font-family: Orbitron, sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: 2px;
    margin-top: -8px;
}

.brand-small span {
    color: var(--cyan);
}

.side-caption {
    text-align: center;
    color: var(--muted);
    font-size: .75rem;
    margin-top: 4px;
}

.nav-title {
    color: #6fdbff;
    font-size: .70rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin: 25px 0 8px;
}

div[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 8px;
}

div[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: linear-gradient(135deg, rgba(16, 22, 37, .95), rgba(10, 14, 25, .95)) !important;
    border: 1px solid rgba(76, 122, 255, .15) !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
    margin: 0 !important;
    color: #aeb8ca !important;
    transition: .25s ease !important;
}

div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    border-color: rgba(0, 210, 255, .65) !important;
    transform: translateX(3px);
}

div[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
    background: linear-gradient(90deg, rgba(24, 112, 255, .92), rgba(117, 48, 238, .92)) !important;
    color: white !important;
    border-color: rgba(116, 192, 255, .7) !important;
    box-shadow: 0 0 22px rgba(71, 100, 255, .25);
}

div[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none;
}

.sidebar-status {
    margin-top: 80px;
    padding: 14px;
    border: 1px solid rgba(83, 130, 255, .20);
    border-radius: 12px;
    background: rgba(10, 14, 25, .8);
}

.dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #20e889;
    border-radius: 50%;
    box-shadow: 0 0 10px #20e889;
    margin-right: 7px;
}

.top-title {
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0;
}

.top-title span {
    color: #39a7ff;
}

.top-subtitle {
    color: #a0aabd;
    font-size: .92rem;
    margin-top: 4px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 8px 12px;
    border: 1px solid rgba(71, 221, 156, .25);
    background: rgba(18, 48, 39, .35);
    border-radius: 999px;
    color: #48e99a;
    font-size: .78rem;
    font-weight: 700;
}

.hero-line {
    height: 1px;
    background: linear-gradient(90deg, rgba(60,120,255,.35), rgba(130,60,255,.22), transparent);
    margin: 18px 0 20px;
}

.action-row {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px !important;
    border: 1px solid rgba(68, 137, 255, .55) !important;
    background: linear-gradient(100deg, #0876df, #5631d6) !important;
    color: white !important;
    font-weight: 700 !important;
    min-height: 42px !important;
    box-shadow: 0 0 18px rgba(47, 128, 255, .16);
    transition: .2s ease !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(103, 67, 255, .35);
}

.metric-card {
    position: relative;
    overflow: hidden;
    min-height: 128px;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(87, 125, 210, .20);
    background: linear-gradient(145deg, rgba(14, 19, 32, .96), rgba(7, 11, 20, .92));
    box-shadow: 0 12px 35px rgba(0,0,0,.24);
}

.metric-card::after {
    content: "";
    position: absolute;
    width: 110px;
    height: 110px;
    right: -35px;
    bottom: -45px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(37, 131, 255, .20), transparent 70%);
}

.metric-label {
    color: #9ca8bc;
    font-size: .78rem;
    font-weight: 700;
}

.metric-value {
    font-family: Orbitron, sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    margin-top: 8px;
}

.metric-foot {
    color: #718097;
    font-size: .72rem;
    margin-top: 8px;
}

.icon-blue { color: #4aa8ff; }
.icon-purple { color: #a871ff; }
.icon-cyan { color: #4de8ff; }

.panel {
    border: 1px solid rgba(88, 130, 230, .20);
    background: linear-gradient(145deg, rgba(11, 16, 28, .96), rgba(6, 10, 18, .96));
    border-radius: 15px;
    padding: 18px;
    box-shadow: 0 15px 40px rgba(0,0,0,.22);
}

.panel-title {
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 4px;
}

.panel-sub {
    color: #77849a;
    font-size: .75rem;
}

.data-title {
    font-size: 1.15rem;
    font-weight: 800;
}

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(76, 122, 255, .20);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stDataFrame"] iframe {
    border-radius: 12px;
}

.stSelectbox label,
.stTextInput label {
    color: #8cdfff !important;
    font-weight: 700 !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #0c111e !important;
    border-color: rgba(76, 122, 255, .25) !important;
}

div[data-baseweb="select"] span {
    color: #e8efff !important;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 800;
    margin: 5px 0 2px;
}

.section-subtitle {
    color: #7d8ba2;
    font-size: .78rem;
    margin-bottom: 12px;
}

.footer {
    color: #59677d;
    font-size: .68rem;
    text-align: center;
    padding: 20px 0 0;
}

div[data-testid="stMetric"] {
    background: transparent;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# FUNÇÕES
# ---------------------------------------------------------
def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=["Data", "Hora", "Peso (kg)", "Lote"])

    df = df.copy()
    renomear = {}
    for c in df.columns:
        chave = str(c).strip().lower().replace(" ", "").replace("_", "")
        if chave == "peso":
            renomear[c] = "Peso (kg)"
        elif chave in {"peso(kg)", "pesokg"}:
            renomear[c] = "Peso (kg)"
        elif chave == "data":
            renomear[c] = "Data"
        elif chave == "hora":
            renomear[c] = "Hora"
        elif chave == "lote":
            renomear[c] = "Lote"
    df = df.rename(columns=renomear)

    for col in ["Data", "Hora", "Peso (kg)", "Lote"]:
        if col not in df.columns:
            df[col] = None

    df["Peso (kg)"] = pd.to_numeric(df["Peso (kg)"], errors="coerce")
    return df[["Data", "Hora", "Peso (kg)", "Lote"]]


@st.cache_data(ttl=10)
def carregar_dados_todas_abas():
    try:
        resposta = requests.get(URL_SCRIPT, timeout=15)
        resposta.raise_for_status()
        dados = resposta.json()

        if not isinstance(dados, dict):
            return {}

        resultado = {}
        for nome_aba, conteudo in dados.items():
            if not isinstance(conteudo, list) or len(conteudo) < 1:
                continue
            cabecalho = conteudo[0]
            linhas = conteudo[1:]
            df = pd.DataFrame(linhas, columns=cabecalho)
            resultado[str(nome_aba)] = normalizar_colunas(df)

        return resultado
    except Exception as erro:
        st.session_state["erro_api"] = str(erro)
        return {}


def obter_df_selecionado(dados, nome):
    return dados.get(nome, pd.DataFrame(columns=["Data", "Hora", "Peso (kg)", "Lote"]))


def exportar_xlsx(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Registros")
        ws = writer.book["Registros"]
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(max(max_len + 2, 12), 28)
    return buffer.getvalue()


def grafico_layout(fig, height=310):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#aeb9cb", family="Inter"),
        margin=dict(l=15, r=15, t=25, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="rgba(90,120,180,.10)", zeroline=False),
        yaxis=dict(gridcolor="rgba(90,120,180,.10)", zeroline=False),
    )
    return fig


def mostrar_metricas(df):
    total = len(df)
    peso_total = float(df["Peso (kg)"].sum()) if not df.empty else 0
    media = float(df["Peso (kg)"].mean()) if not df.empty else 0
    maior = float(df["Peso (kg)"].max()) if not df.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("📦", "Total de Lotes", f"{total:,}".replace(",", "."), "Registros no dia", "blue"),
        ("⚖", "Peso Total (kg)", f"{peso_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "Produção registrada", "cyan"),
        ("◈", "Média por Lote", f"{media:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", "."), "Média dos registros", "purple"),
        ("↑", "Maior Peso", f"{maior:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", "."), "Maior registro do dia", "purple"),
    ]

    for col, (icon, label, value, foot, color) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label"><span class="icon-{color}">{icon}</span>&nbsp;&nbsp;{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-foot">{foot}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)
    else:
        st.markdown("<div class='brand-small'>A<span>Mi</span>RA</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='brand-small'>Sistema <span>AMIRA</span></div>"
        "<div class='side-caption'>Monitoramento • Automação • Precisão</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='nav-title'>MENU DE NAVEGAÇÃO</div>", unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        ["📋  Registro e Dados", "📊  Gráficos e Análises", "＋  Nova Aba"],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="sidebar-status">
            <div style="font-weight:800;">Sistema AMIRA</div>
            <div style="color:#7f8da4;font-size:.75rem;margin-top:5px;">
                <span class="dot"></span>Conectado ao monitoramento
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='footer'>© 2026 AMIRA • SENAI<br>IoT • Automação • Precisão</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# CABEÇALHO
# ---------------------------------------------------------
header_left, header_right = st.columns([3.2, 1.5])

with header_left:
    st.markdown(
        """
        <div class="top-title">Bem-vindo ao <span>AMIRA</span></div>
        <div class="top-subtitle">Sistema de Monitoramento e Registro de Produção</div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    h1, h2 = st.columns(2)
    with h1:
        st.markdown("<div class='status-pill'>● Online</div>", unsafe_allow_html=True)
    with h2:
        if st.button("↻  Recarregar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

st.markdown("<div class='hero-line'></div>", unsafe_allow_html=True)

dados_abas = carregar_dados_todas_abas()

# Ordena datas no formato dd-MM-yyyy quando possível
def chave_aba(nome):
    try:
        return datetime.strptime(nome, "%d-%m-%Y")
    except Exception:
        return datetime.min

lista_abas = sorted(dados_abas.keys(), key=chave_aba, reverse=True)

if "erro_api" in st.session_state and not dados_abas:
    st.warning("Não foi possível atualizar os dados agora. Verifique se o Google Apps Script está publicado como aplicativo da Web.")

# ---------------------------------------------------------
# REGISTRO E DADOS
# ---------------------------------------------------------
if menu == "📋  Registro e Dados":
    if not lista_abas:
        st.info("Aguardando dados da balança. Quando o primeiro registro for enviado, o AMIRA criará automaticamente a aba do dia.")
    else:
        dia = st.selectbox("Dia de produção", lista_abas, index=0)
        df = obter_df_selecionado(dados_abas, dia)

        mostrar_metricas(df)
        st.markdown("<br>", unsafe_allow_html=True)

        left, right = st.columns([3.3, 1])
        with left:
            st.markdown(
                f"""
                <div class="panel">
                    <div class="data-title">Dados do Dia</div>
                    <div class="panel-sub">Registros da produção • {dia}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            xlsx = exportar_xlsx(df)
            st.download_button(
                "↓  Baixar Planilha",
                data=xlsx,
                file_name=f"AMIRA_{dia}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if df.empty:
            st.info("A aba selecionada ainda não possui registros.")
        else:
            st.dataframe(
                df,
                use_container_width=True,
                height=420,
                hide_index=True,
                column_config={
                    "Data": st.column_config.TextColumn("Data"),
                    "Hora": st.column_config.TextColumn("Hora"),
                    "Peso (kg)": st.column_config.NumberColumn("Peso (kg)", format="%.2f"),
                    "Lote": st.column_config.TextColumn("Lote"),
                },
            )

        # Resumo visual
        st.markdown("<br>", unsafe_allow_html=True)
        a, b = st.columns([2, 1])

        with a:
            st.markdown("<div class='section-title'>Evolução dos Pesos</div><div class='section-subtitle'>Acompanhamento dos registros ao longo do dia</div>", unsafe_allow_html=True)
            if not df.empty:
                dfg = df.reset_index(drop=True).copy()
                dfg["Registro"] = dfg.index + 1
                fig = px.line(dfg, x="Registro", y="Peso (kg)", markers=True)
                fig.update_traces(line_color="#3d8cff", marker_color="#a16bff", line_width=3)
                st.plotly_chart(grafico_layout(fig), use_container_width=True)
            else:
                st.info("Sem dados suficientes para gerar o gráfico.")

        with b:
            st.markdown("<div class='section-title'>Resumo do Dia</div><div class='section-subtitle'>Indicadores principais</div>", unsafe_allow_html=True)
            peso_total = float(df["Peso (kg)"].sum()) if not df.empty else 0
            media = float(df["Peso (kg)"].mean()) if not df.empty else 0
            menor = float(df["Peso (kg)"].min()) if not df.empty else 0
            maior = float(df["Peso (kg)"].max()) if not df.empty else 0

            st.markdown(
                f"""
                <div class="panel">
                    <div style="font-size:1.8rem;font-family:Orbitron;font-weight:700;color:#58b7ff;">{peso_total:.2f} kg</div>
                    <div style="color:#7f8da4;font-size:.75rem;">peso total registrado</div>
                    <hr style="border-color:rgba(90,120,180,.12);">
                    <div style="display:flex;justify-content:space-between;margin:9px 0;"><span style="color:#8290a7;">Média</span><b>{media:.2f} kg</b></div>
                    <div style="display:flex;justify-content:space-between;margin:9px 0;"><span style="color:#8290a7;">Maior</span><b>{maior:.2f} kg</b></div>
                    <div style="display:flex;justify-content:space-between;margin:9px 0;"><span style="color:#8290a7;">Menor</span><b>{menor:.2f} kg</b></div>
                    <div style="display:flex;justify-content:space-between;margin:9px 0;"><span style="color:#8290a7;">Registros</span><b>{len(df)}</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------
# GRÁFICOS E ANÁLISES
# ---------------------------------------------------------
elif menu == "📊  Gráficos e Análises":
    st.markdown("<div class='section-title'>Gráficos e Análises</div><div class='section-subtitle'>Transforme os registros da balança em informações visuais para tomada de decisão.</div>", unsafe_allow_html=True)

    if not lista_abas:
        st.info("Aguardando registros para gerar as análises.")
    else:
        dia = st.selectbox("Dia analisado", lista_abas, index=0)
        df = obter_df_selecionado(dados_abas, dia)

        mostrar_metricas(df)
        st.markdown("<br>", unsafe_allow_html=True)

        if not df.empty:
            c1, c2 = st.columns(2)

            with c1:
                dfg = df.reset_index(drop=True).copy()
                dfg["Registro"] = dfg.index + 1
                fig = px.area(dfg, x="Registro", y="Peso (kg)")
                fig.update_traces(line_color="#3d8cff", fillcolor="rgba(61,140,255,.15)")
                st.markdown("<div class='panel-title'>Peso ao longo do dia</div>", unsafe_allow_html=True)
                st.plotly_chart(grafico_layout(fig), use_container_width=True)

            with c2:
                fig2 = px.histogram(df, x="Peso (kg)", nbins=8)
                fig2.update_traces(marker_color="#7d4cff")
                st.markdown("<div class='panel-title'>Distribuição dos pesos</div>", unsafe_allow_html=True)
                st.plotly_chart(grafico_layout(fig2), use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Comparação entre dias
            resumo = []
            for nome, temp in dados_abas.items():
                if not temp.empty:
                    resumo.append({
                        "Data": nome,
                        "Peso total (kg)": temp["Peso (kg)"].sum(),
                        "Média (kg)": temp["Peso (kg)"].mean(),
                        "Lotes": len(temp),
                    })

            resumo_df = pd.DataFrame(resumo)

            if not resumo_df.empty:
                c3, c4 = st.columns(2)
                with c3:
                    fig3 = px.bar(resumo_df, x="Data", y="Peso total (kg)")
                    fig3.update_traces(marker_color="#2f80ff")
                    st.markdown("<div class='panel-title'>Peso total por dia</div>", unsafe_allow_html=True)
                    st.plotly_chart(grafico_layout(fig3), use_container_width=True)

                with c4:
                    fig4 = px.bar(resumo_df, x="Data", y="Lotes")
                    fig4.update_traces(marker_color="#8a35ff")
                    st.markdown("<div class='panel-title'>Quantidade de lotes por dia</div>", unsafe_allow_html=True)
                    st.plotly_chart(grafico_layout(fig4), use_container_width=True)

# ---------------------------------------------------------
# NOVA ABA
# ---------------------------------------------------------
else:
    st.markdown("<div class='section-title'>Nova Aba</div><div class='section-subtitle'>Crie manualmente uma aba na planilha. O sistema também cria automaticamente a aba do dia quando a balança envia o primeiro registro.</div>", unsafe_allow_html=True)

    with st.form("form_nova_aba"):
        nome = st.text_input("Nome da nova aba", placeholder="Ex.: 18-08-2026")
        enviar = st.form_submit_button("＋  Criar Nova Aba", use_container_width=True)

        if enviar:
            nome = nome.strip()
            if not nome:
                st.warning("Digite um nome para a aba.")
            else:
                try:
                    resposta = requests.post(
                        URL_SCRIPT,
                        json={"action": "criar_aba", "nome_aba": nome},
                        timeout=15,
                    )
                    resposta.raise_for_status()
                    resultado = resposta.text
                    st.success(f"Aba '{nome}' criada com sucesso.")
                    st.cache_data.clear()
                except Exception as erro:
                    st.error(f"Não foi possível criar a aba: {erro}")

st.markdown(
    "<div class='footer'>AMIRA • Sistema de Monitoramento e Registro de Produção • SENAI</div>",
    unsafe_allow_html=True,
)
