import io
import os
import re
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(
    page_title="AMIRA | Monitoramento de Produção",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# SUBSTITUA PELA SUA URL DO GOOGLE APPS SCRIPT
URL_SCRIPT = "https://script.google.com/macros/s/AKfycbwQ8IIVRIDsx8-CdJeKw6LUr4rBOFGX0jb42augc8v89TZVNWy0O8mlBAK23O2Tjymmaw/exec"
TZ = "America/Sao_Paulo"

# =========================================================
# VISUAL AMIRA (CSS)
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@600;700;800&display=swap');
:root{--bg:#05070d;--panel:#0b0f1a;--panel2:#0f1422;--line:rgba(85,139,255,.24);--blue:#2f80ff;--cyan:#00d2ff;--purple:#8a35ff;--text:#f4f7ff;--muted:#8f9bb2}
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:radial-gradient(circle at 68% 12%,rgba(54,83,180,.13),transparent 28%),radial-gradient(circle at 96% 76%,rgba(138,53,255,.12),transparent 31%),#05070d;color:var(--text)}
header[data-testid="stHeader"]{background:transparent!important}
[data-testid="stToolbar"]{display:flex!important;background:transparent!important}
[data-testid="stDecoration"]{display:none!important}
[data-testid="stHeader"] button,[data-testid="stToolbar"] button{display:inline-flex!important;visibility:visible!important;opacity:1!important;color:#dbeaff!important;background:rgba(10,15,29,.92)!important;border:1px solid rgba(76,145,255,.65)!important;border-radius:9px!important;box-shadow:0 0 18px rgba(58,116,255,.28)!important}
[data-testid="stSidebarCollapsedControl"]{display:flex!important;position:fixed!important;top:.55rem!important;left:.7rem!important;z-index:100000!important;background:rgba(10,15,29,.92)!important;border:1px solid rgba(76,145,255,.65)!important;border-radius:9px!important;box-shadow:0 0 18px rgba(58,116,255,.28)!important}
.block-container{padding:1.25rem 1.6rem 2rem;max-width:1700px}
section[data-testid="stSidebar"]{background:radial-gradient(circle at 50% 12%,rgba(50,117,255,.12),transparent 25%),linear-gradient(180deg,#070a12 0%,#080b14 100%)!important;border-right:1px solid rgba(76,122,255,.18)}
section[data-testid="stSidebar"]>div{padding-top:1.05rem}
.sidebar-logo{width:100%;max-height:185px;object-fit:contain;border-radius:16px;filter:drop-shadow(0 0 18px rgba(45,126,255,.16))}
.brand-small{text-align:center;font-family:Orbitron,sans-serif;font-size:1.05rem;font-weight:800;letter-spacing:2px;margin-top:-7px}.brand-small span{color:var(--cyan)}
.side-caption{text-align:center;color:var(--muted);font-size:.75rem;margin-top:4px}
.nav-title{color:#6fdbff;font-size:.70rem;font-weight:800;letter-spacing:1.5px;margin:25px 0 8px}
div[data-testid="stSidebar"] div[role="radiogroup"]{gap:10px;width:100%}
section[data-testid="stSidebar"] .stButton{width:100%!important;margin:0 0 10px!important}
section[data-testid="stSidebar"] .stButton>button{width:100%!important;min-height:58px!important;padding:14px 16px!important;justify-content:flex-start!important;text-align:left!important;border-radius:10px!important;border:1px solid rgba(76,122,255,.24)!important;background:linear-gradient(135deg,rgba(16,22,37,.98),rgba(10,14,25,.98))!important;color:#dce6fa!important;font-size:.92rem!important;font-weight:750!important;box-shadow:none!important}
section[data-testid="stSidebar"] .stButton>button:hover{border-color:rgba(0,210,255,.75)!important;transform:translateX(3px)!important;box-shadow:0 0 20px rgba(33,133,255,.20)!important}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:linear-gradient(90deg,rgba(21,116,255,.98),rgba(112,49,235,.98))!important;color:white!important;border-color:rgba(138,201,255,.8)!important;box-shadow:0 0 22px rgba(71,100,255,.30)!important}
.sidebar-status{margin-top:55px;padding:14px;border:1px solid rgba(83,130,255,.20);border-radius:12px;background:rgba(10,14,25,.8)}
.dot{display:inline-block;width:8px;height:8px;background:#20e889;border-radius:50%;box-shadow:0 0 10px #20e889;margin-right:7px}
.top-title{font-size:1.8rem;font-weight:800;margin:0}.top-title span{color:#39a7ff}.top-subtitle{color:#a0aabd;font-size:.92rem;margin-top:4px}
.status-pill{display:inline-flex;align-items:center;gap:5px;padding:8px 12px;border:1px solid rgba(71,221,156,.25);background:rgba(18,48,39,.35);border-radius:999px;color:#48e99a;font-size:.78rem;font-weight:700}
.hero-line{height:1px;background:linear-gradient(90deg,rgba(60,120,255,.35),rgba(130,60,255,.22),transparent);margin:16px 0 18px}
.stButton>button,.stDownloadButton>button{border-radius:10px!important;border:1px solid rgba(68,137,255,.55)!important;background:linear-gradient(100deg,#0876df,#5631d6)!important;color:#fff!important;font-weight:700!important;min-height:42px!important;box-shadow:0 0 18px rgba(47,128,255,.16);transition:.2s ease!important}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:0 0 25px rgba(103,67,255,.35)}
.metric-card{position:relative;overflow:hidden;min-height:118px;padding:18px;border-radius:15px;border:1px solid rgba(87,125,210,.22);background:linear-gradient(145deg,rgba(14,19,32,.97),rgba(7,11,20,.92));box-shadow:0 12px 35px rgba(0,0,0,.24);transition:.25s ease}
.metric-card:hover{transform:translateY(-2px);border-color:rgba(70,157,255,.45);box-shadow:0 16px 40px rgba(25,75,170,.18)}
.metric-card:after{content:"";position:absolute;width:115px;height:115px;right:-38px;bottom:-48px;border-radius:50%;background:radial-gradient(circle,rgba(37,131,255,.20),transparent 70%)}
.metric-label{color:#9ca8bc;font-size:.78rem;font-weight:700}.metric-value{font-family:Orbitron,sans-serif;font-size:1.7rem;font-weight:700;margin-top:8px}.metric-foot{color:#718097;font-size:.72rem;margin-top:7px}
.icon-blue{color:#4aa8ff}.icon-purple{color:#a871ff}.icon-cyan{color:#4de8ff}
.panel{border:1px solid rgba(88,130,230,.20);background:linear-gradient(145deg,rgba(11,16,28,.97),rgba(6,10,18,.97));border-radius:15px;padding:16px;box-shadow:0 15px 40px rgba(0,0,0,.22)}
.panel-title{font-size:1rem;font-weight:800;margin-bottom:4px}.panel-sub{color:#77849a;font-size:.75rem}.data-title{font-size:1.15rem;font-weight:800}.section-title{font-size:1.22rem;font-weight:800;margin:5px 0 2px}.section-subtitle{color:#7d8ba2;font-size:.78rem;margin-bottom:12px}
.summary-panel{height:100%;min-height:390px}.summary-row{display:flex;justify-content:space-between;gap:12px;margin:12px 0;color:#8290a7;font-size:.8rem}.summary-row b{color:#f3f6ff}
[data-testid="stDataFrame"]{border:1px solid rgba(76,122,255,.20);border-radius:12px;overflow:hidden}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{background:#0c111e!important;border-color:rgba(76,122,255,.25)!important}div[data-baseweb="select"] span{color:#e8efff!important}
.stSelectbox label,.stTextInput label{color:#8cdfff!important;font-weight:700!important}
.footer{color:#59677d;font-size:.68rem;text-align:center;padding:20px 0 0}
.small-note{color:#6f7e96;font-size:.72rem}
.automation-note{display:flex;align-items:center;gap:10px;margin:18px 0 8px;padding:13px 15px;border:1px solid rgba(73,215,154,.25);border-radius:11px;background:linear-gradient(90deg,rgba(19,66,55,.30),rgba(12,22,38,.65));color:#b8c8da;font-size:.80rem}.automation-note b{color:#53efa5}
[data-testid="stExpander"]{border:1px solid rgba(83,130,255,.25)!important;border-radius:11px!important;background:rgba(10,15,27,.70)!important;margin-bottom:9px!important}[data-testid="stExpander"] summary{font-weight:750!important;color:#e9f1ff!important}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# FUNÇÕES DE TRATAMENTO DE DADOS
# =========================================================
def vazio():
    return pd.DataFrame(columns=["Data", "Hora", "Peso (kg)", "Lote"])


def formatar_data_planilha(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return None
    texto = str(valor).strip()
    try:
        if "T" in texto or texto.endswith("Z"):
            data = pd.to_datetime(texto, utc=True, errors="coerce")
            if not pd.isna(data):
                return data.tz_convert(TZ).strftime("%d/%m/%Y")
        data = pd.to_datetime(texto, errors="coerce", dayfirst=True)
        if not pd.isna(data):
            return data.strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        pass
    return texto


def formatar_hora_planilha(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return None
    texto = str(valor).strip()
    marco_excel = re.match(r"^1899-12-\d{2}T(\d{2}:\d{2}:\d{2})", texto)
    if marco_excel:
        return marco_excel.group(1)
    hora = re.match(r"^(\d{1,2}:\d{2}(?::\d{2})?)$", texto)
    if hora:
        partes = hora.group(1).split(":")
        return f"{int(partes[0]):02d}:{partes[1]}:{partes[2] if len(partes) == 3 else '00'}"
    try:
        data = pd.to_datetime(texto, utc=True, errors="coerce")
        if not pd.isna(data):
            return data.tz_convert(TZ).strftime("%H:%M:%S")
    except (TypeError, ValueError):
        pass
    return texto


def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return vazio()
    df = df.copy()
    renomear = {}
    for c in df.columns:
        chave = str(c).strip().lower().replace(" ", "").replace("_", "")
        if chave in {"peso", "peso(kg)", "pesokg"}:
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
    df["Data"] = df["Data"].map(formatar_data_planilha)
    df["Hora"] = df["Hora"].map(formatar_hora_planilha)
    return df[["Data", "Hora", "Peso (kg)", "Lote"]].dropna(subset=["Peso (kg)"], how="all")


@st.cache_data(ttl=15)
def carregar_dados_todas_abas():
    resposta = requests.get(URL_SCRIPT, timeout=20)
    resposta.raise_for_status()
    dados = resposta.json()
    if not isinstance(dados, dict):
        raise ValueError("O Google Apps Script não devolveu um JSON de abas.")
    resultado = {}
    for nome_aba, conteudo in dados.items():
        if not isinstance(conteudo, list) or not conteudo:
            continue
        cabecalho = conteudo[0]
        linhas = conteudo[1:]
        if not isinstance(cabecalho, list):
            continue
        resultado[str(nome_aba)] = normalizar_colunas(pd.DataFrame(linhas, columns=cabecalho))
    return resultado


def chave_aba(nome):
    data = data_da_aba(nome)
    return datetime.combine(data, datetime.min.time()) if data else datetime.min


def data_da_aba(nome):
    texto = str(nome)
    for padrao, formato in [
        (r"(?<!\d)(\d{2}-\d{2}-\d{4})(?!\d)", "%d-%m-%Y"),
        (r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)", "%Y-%m-%d"),
    ]:
        encontrado = re.search(padrao, texto)
        if encontrado:
            try:
                return datetime.strptime(encontrado.group(1), formato).date()
            except ValueError:
                pass
    return None


def rotulo_aba(nome):
    data = data_da_aba(nome)
    return data.strftime("%d/%m/%Y") if data else str(nome)


def formatar_numero(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_xlsx(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
        wb = Workbook()
        ws = wb.active
        ws.title = "Registros"
        cab = list(df.columns)
        ws.append(cab)
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="111827")
        for row in df.itertuples(index=False, name=None):
            ws.append(list(row))
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for col in ws.columns:
            letra = col[0].column_letter
            maior = max(len(str(c.value or "")) for c in col)
            ws.column_dimensions[letra].width = min(max(maior + 2, 12), 28)
        wb.save(buffer)
        return buffer.getvalue()
    except Exception:
        return df.to_csv(index=False, sep=";").encode("utf-8-sig")


def grafico_layout(fig, height=300):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#aeb9cb", family="Inter"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=height,
        showlegend=False,
        xaxis=dict(gridcolor="rgba(90,120,180,.10)", zeroline=False),
        yaxis=dict(gridcolor="rgba(90,120,180,.10)", zeroline=False),
    )
    return fig


def mostrar_metricas(df):
    total_caixas = len(df)
    peso_total = float(df["Peso (kg)"].sum()) if not df.empty else 0
    media = float(df["Peso (kg)"].mean()) if not df.empty else 0
    
    cards = [
        ("📦", "Caixas Passadas", f"{total_caixas}", "Hoje", "cyan"),
        ("⚖", "Peso Total (kg)", formatar_numero(peso_total), "Hoje", "blue"),
        ("◈", "Média por Caixa", f"{formatar_numero(media)} kg", "Hoje", "purple"),
    ]
    cols = st.columns(3)
    for col, (icon, label, value, foot, color) in zip(cols, cards):
        with col:
            st.markdown(
                f"<div class='metric-card'>"
                f"<div class='metric-label'><span class='icon-{color}'>{icon}</span>&nbsp;&nbsp;{label}</div>"
                f"<div class='metric-value'>{value}</div>"
                f"<div class='metric-foot'>{foot}</div>"
                f"</div>",
                unsafe_allow_html=True
            )


def resumo_dia(df):
    peso_total = float(df["Peso (kg)"].sum()) if not df.empty else 0
    media = float(df["Peso (kg)"].mean()) if not df.empty else 0
    total_caixas = len(df)
    return peso_total, media, total_caixas


def grafico_distribuicao(df):
    if df.empty:
        return None
    bins = [0, 50, 60, 70, 80, float("inf")]
    labels = ["< 50 kg", "50 – 60 kg", "60 – 70 kg", "70 – 80 kg", "80+ kg"]
    grupos = pd.cut(df["Peso (kg)"], bins=bins, labels=labels, right=False)
    contagem = grupos.value_counts().reindex(labels, fill_value=0)
    fig = go.Figure(go.Pie(labels=contagem.index, values=contagem.values, hole=.72, textinfo="none", marker=dict(colors=["#2f80ff", "#4b6cff", "#713dff", "#8a35ff", "#b64dff"])))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=250, margin=dict(l=5,r=5,t=5,b=5), showlegend=False, annotations=[dict(text=f"{len(df)}<br>caixas", x=.5, y=.5, font=dict(size=20, color="#fff"), showarrow=False)])
    return fig, contagem

# =========================================================
# CARREGAMENTO (SEM SIMULAÇÃO)
# =========================================================
try:
    dados_abas = carregar_dados_todas_abas()
    erro_api = None
except Exception as erro:
    dados_abas = {}
    erro_api = str(erro)

lista_abas = sorted(dados_abas.keys(), key=chave_aba, reverse=True)
if lista_abas:
    dia_atual = st.session_state.get("dia_selecionado", lista_abas[0])
    if dia_atual not in lista_abas:
        dia_atual = lista_abas[0]
else:
    dia_atual = None

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)
    st.markdown("<div class='brand-small'>Sistema <span>AMIRA</span></div><div class='side-caption'>Monitoramento • Automação • Precisão</div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-title'>MENU DE NAVEGAÇÃO</div>", unsafe_allow_html=True)
    opcoes_menu = ["📋  Registro e Dados", "📊  Gráficos e Análises", "🗂  Histórico de Planilhas"]
    menu = st.session_state.get("menu_amira", opcoes_menu[0])
    for indice, opcao in enumerate(opcoes_menu):
        if st.button(
            opcao,
            key=f"menu_amira_{indice}",
            type="primary" if menu == opcao else "secondary",
            use_container_width=True,
        ):
            st.session_state["menu_amira"] = opcao
            st.rerun()
    st.markdown("<div class='sidebar-status'><div style='font-weight:800;'>Sistema AMIRA</div><div style='color:#7f8da4;font-size:.75rem;margin-top:5px;'><span class='dot'></span>Monitoramento ativo</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>© 2026 AMIRA • SENAI<br>IoT • Automação • Precisão</div>", unsafe_allow_html=True)

# =========================================================
# CABEÇALHO + AÇÕES
# =========================================================
header_left, header_right = st.columns([2.9, 2.1])
with header_left:
    st.markdown("<div class='top-title'>Bem-vindo ao <span>AMIRA</span></div><div class='top-subtitle'>Sistema de Monitoramento e Registro de Produção</div>", unsafe_allow_html=True)
with header_right:
    a, b, c = st.columns([1, 1.45, 1.45])
    with a:
        st.markdown("<div class='status-pill'>● Online</div>", unsafe_allow_html=True)
    with b:
        if st.button("↻  Recarregar Planilha", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with c:
        if dia_atual:
            df_download = dados_abas.get(dia_atual, vazio())
            st.download_button("↓  Baixar Planilha", data=gerar_xlsx(df_download), file_name=f"AMIRA_{dia_atual}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        else:
            st.button("↓  Baixar Planilha", disabled=True, use_container_width=True)

st.markdown("<div class='hero-line'></div>", unsafe_allow_html=True)
if erro_api:
    st.warning("Não foi possível atualizar os dados da planilha agora. O painel continua funcionando e não será derrubado pelo erro de exportação. Verifique a publicação do Google Apps Script.")

# =========================================================
# REGISTRO E DADOS — LAYOUT PRINCIPAL
# =========================================================
if menu == "📋  Registro e Dados":
    if not lista_abas:
        st.info("Aguardando dados da balança. Quando o primeiro registro for enviado, o AMIRA criará automaticamente a aba do dia.")
    else:
        seletor_col, vazio_col = st.columns([1.1, 3.9])
        with seletor_col:
            dia = st.selectbox("Data de produção", lista_abas, index=lista_abas.index(dia_atual))
            st.session_state["dia_selecionado"] = dia
        df = dados_abas.get(dia, vazio())

        mostrar_metricas(df)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div class='panel'><div class='data-title'>Dados do Dia</div><div class='panel-sub'>Registros da produção • <b style='color:#dce7ff'>" + str(dia) + "</b></div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        left, right = st.columns([3.35, 1.05])

        with left:
            if df.empty:
                st.info("A aba selecionada ainda não possui registros.")
            else:
                page_size = 7
                total_pages = max(1, (len(df) + page_size - 1) // page_size)
                page_key = f"page_{dia}"
                pagina = int(st.session_state.get(page_key, 0))
                pagina = min(pagina, total_pages - 1)
                inicio = pagina * page_size
                tabela = df.iloc[inicio:inicio + page_size].copy()
                tabela.insert(0, "#", range(inicio + 1, inicio + len(tabela) + 1))
                st.dataframe(tabela, use_container_width=True, height=390, hide_index=True, column_config={"#": st.column_config.NumberColumn("#", width="small"), "Data": st.column_config.TextColumn("Data"), "Hora": st.column_config.TextColumn("Hora"), "Peso (kg)": st.column_config.NumberColumn("Peso (kg)", format="%.2f"), "Lote": st.column_config.TextColumn("Lote")})
                p1, p2, p3 = st.columns([2.2, 2.2, 2.2])
                with p1:
                    st.caption(f"Mostrando {inicio+1} a {min(inicio+page_size,len(df))} de {len(df)} registros")
                with p2:
                    st.caption(f"Página {pagina+1} de {total_pages}")
                with p3:
                    q1, q2 = st.columns(2)
                    with q1:
                        if st.button("‹", key=f"prev_{dia}", disabled=pagina == 0, use_container_width=True):
                            st.session_state[page_key] = max(0, pagina - 1); st.rerun()
                    with q2:
                        if st.button("›", key=f"next_{dia}", disabled=pagina >= total_pages - 1, use_container_width=True):
                            st.session_state[page_key] = min(total_pages - 1, pagina + 1); st.rerun()

        with right:
            peso_total, media, total_caixas = resumo_dia(df)
            st.markdown("<div class='panel summary-panel'><div class='panel-title'>Resumo do Dia</div><div class='panel-sub'>Indicadores principais</div>", unsafe_allow_html=True)
            ring = go.Figure(go.Pie(values=[max(peso_total, 0.001), 1], labels=["Total", ""], hole=.78, textinfo="none", marker=dict(colors=["#3d8cff", "#7d32ff"], line=dict(color="#0a0e18", width=4))))
            ring.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0), height=175, showlegend=False, annotations=[dict(text=f"{formatar_numero(peso_total)}<br><span style='font-size:12px'>kg</span>", x=.5, y=.5, font=dict(size=19,color="#fff"), showarrow=False)])
            st.plotly_chart(ring, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                f"<div class='summary-row'><span>📦 Caixas passadas</span><b>{total_caixas}</b></div>"
                f"<div class='summary-row'><span>↗ Média por caixa</span><b>{formatar_numero(media)} kg</b></div>"
                f"<div class='summary-row'><span>⚖ Peso total acumulado</span><b>{formatar_numero(peso_total)} kg</b></div></div>", 
                unsafe_allow_html=True
            )

        st.markdown("<div class='automation-note'>✓ <span><b>Novo dia automático:</b> a planilha do próximo dia é criada pela balança assim que a primeira pesagem é enviada. Não é preciso criar uma aba manualmente.</span></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title' style='font-size:1.18rem'>Visão Geral</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Análise visual da produção do dia</div>", unsafe_allow_html=True)
        g1, g2, g3 = st.columns(3)
        with g1:
            st.markdown("<div class='panel-title'>Peso ao longo do dia (kg)</div>", unsafe_allow_html=True)
            if not df.empty:
                dfg = df.reset_index(drop=True).copy(); dfg["Registro"] = dfg.index + 1
                fig = px.line(dfg, x="Registro", y="Peso (kg)", markers=True)
                fig.update_traces(line_color="#3d8cff", marker_color="#a16bff", line_width=3)
                st.plotly_chart(grafico_layout(fig, 270), use_container_width=True, config={"displayModeBar": False})
            else: st.info("Sem dados")
        with g2:
            st.markdown("<div class='panel-title'>Distribuição de peso (kg)</div>", unsafe_allow_html=True)
            dist = grafico_distribuicao(df)
            if dist:
                fig, contagem = dist
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.markdown("<div class='small-note'>" + " • ".join([f"{k}: {v}" for k,v in contagem.items() if v]) + "</div>", unsafe_allow_html=True)
            else: st.info("Sem dados")
        with g3:
            st.markdown("<div class='panel-title'>Caixas por período</div>", unsafe_allow_html=True)
            if not df.empty:
                temp = df.copy(); temp["Hora_dt"] = pd.to_datetime(temp["Hora"].astype(str), errors="coerce")
                temp["Hora"] = temp["Hora_dt"].dt.hour
                por_hora = temp.dropna(subset=["Hora"]).groupby("Hora").size().reset_index(name="Caixas")
                fig = px.bar(por_hora, x="Hora", y="Caixas")
                fig.update_traces(marker_color="#713dff")
                fig.update_xaxes(dtick=1)
                st.plotly_chart(grafico_layout(fig, 270), use_container_width=True, config={"displayModeBar": False})
            else: st.info("Sem dados")

# =========================================================
# GRÁFICOS E ANÁLISES
# =========================================================
elif menu == "📊  Gráficos e Análises":
    st.markdown("<div class='section-title'>Gráficos e Análises</div><div class='section-subtitle'>Explore o histórico e compare dias de produção.</div>", unsafe_allow_html=True)
    if not lista_abas:
        st.info("Aguardando registros para gerar as análises.")
    else:
        dia = st.selectbox("Dia analisado", lista_abas, index=lista_abas.index(dia_atual))
        df = dados_abas.get(dia, vazio())
        mostrar_metricas(df)
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='panel-title'>Peso ao longo do dia</div>", unsafe_allow_html=True)
            if not df.empty:
                dfg=df.reset_index(drop=True).copy(); dfg["Registro"]=dfg.index+1
                fig=px.area(dfg,x="Registro",y="Peso (kg)"); fig.update_traces(line_color="#3d8cff",fillcolor="rgba(61,140,255,.15)")
                st.plotly_chart(grafico_layout(fig),use_container_width=True,config={"displayModeBar":False})
        with c2:
            st.markdown("<div class='panel-title'>Distribuição dos pesos</div>", unsafe_allow_html=True)
            if not df.empty:
                fig=px.histogram(df,x="Peso (kg)",nbins=8); fig.update_traces(marker_color="#7d4cff")
                st.plotly_chart(grafico_layout(fig),use_container_width=True,config={"displayModeBar":False})
        resumo=[]
        for nome,temp in dados_abas.items():
            if not temp.empty: resumo.append({"Data":nome,"Peso total (kg)":temp["Peso (kg)"].sum(),"Média (kg)":temp["Peso (kg)"].mean(),"Caixas":len(temp)})
        rdf=pd.DataFrame(resumo)
        if not rdf.empty:
            c3,c4=st.columns(2)
            with c3:
                fig=px.bar(rdf,x="Data",y="Peso total (kg)"); fig.update_traces(marker_color="#2f80ff")
                st.plotly_chart(grafico_layout(fig),use_container_width=True,config={"displayModeBar":False})
            with c4:
                fig=px.bar(rdf,x="Data",y="Caixas"); fig.update_traces(marker_color="#8a35ff")
                st.plotly_chart(grafico_layout(fig),use_container_width=True,config={"displayModeBar":False})

# =========================================================
# HISTÓRICO DE PLANILHAS (FUNDO VERDE SUAVE)
# =========================================================
else:
    st.markdown("<div class='section-title'>Histórico de Planilhas</div><div class='section-subtitle'>Histórico de todas as planilhas registradas no sistema.</div>", unsafe_allow_html=True)
    
    # CSS injetado apenas nesta página para deixar os botões (expanders) com verde suave
    st.markdown("""
    <style>
    [data-testid="stExpander"] {
        background: rgba(35, 110, 60, 0.2) !important;
        border: 1px solid rgba(46, 204, 113, 0.4) !important;
        transition: 0.3s ease;
    }
    [data-testid="stExpander"]:hover {
        background: rgba(35, 110, 60, 0.35) !important;
        border-color: rgba(46, 204, 113, 0.7) !important;
    }
    [data-testid="stExpander"] summary p {
        color: #c4f3d2 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stExpander"] summary svg {
        color: #c4f3d2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if not lista_abas:
        st.info("Ainda não há planilhas lançadas. Quando houver envios da balança, elas aparecerão aqui.")
    else:
        for nome in sorted(lista_abas, key=chave_aba, reverse=True):
            temp = dados_abas.get(nome, vazio())
            rotulo = rotulo_aba(nome)
            
            # Título limpo: apenas o ícone e o nome da aba
            with st.expander(f"📄 {rotulo}", expanded=False):
                if temp.empty:
                    st.info("A planilha existe, mas ainda não possui registros.")
                else:
                    tabela_historico = temp.copy().reset_index(drop=True)
                    tabela_historico.insert(0, "#", tabela_historico.index + 1)
                    st.dataframe(
                        tabela_historico, 
                        use_container_width=True, 
                        hide_index=True, 
                        column_config={
                            "#": st.column_config.NumberColumn("#", width="small"), 
                            "Peso (kg)": st.column_config.NumberColumn("Peso (kg)", format="%.2f")
                        }
                    )

st.markdown("<div class='footer'>AMIRA • Sistema de Monitoramento e Registro de Produção • SENAI</div>", unsafe_allow_html=True)
