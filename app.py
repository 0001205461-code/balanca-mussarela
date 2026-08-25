import io
import os
import re
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
page_title="AMIRA | Monitoramento de Produção",
page_icon="⚡",
layout="wide",
initial_sidebar_state="expanded",
)

URL_SCRIPT = (
"https://script.google.com/macros/s/"
"AKfycbwQ8IIVRIDsx8-CdJeKw6LUr4rBOFGX0jb42augc8v89"
"TZVNWy0O8mlBAK23O2Tjymmaw/exec"
)

TZ = "America/Sao_Paulo"


# =========================================================
# VISUAL AMIRA
# =========================================================

st.markdown(
"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@600;700;800&display=swap');

:root{
--bg:#05070d;
--panel:#0b0f1a;
--panel2:#0f1422;
--line:rgba(85,139,255,.24);
--blue:#2f80ff;
--cyan:#00d2ff;
--purple:#8a35ff;
--green:#20e889;
--text:#f4f7ff;
--muted:#8f9bb2;
}


/* =====================================================
BASE
===================================================== */

html,
body,
[class*="css"]{
font-family:Inter,sans-serif;
}

.stApp{
background:
radial-gradient(
circle at 68% 12%,
rgba(54,83,180,.13),
transparent 28%
),
radial-gradient(
circle at 96% 76%,
rgba(138,53,255,.12),
transparent 31%
),
#05070d !important;

color:var(--text);
}

header[data-testid="stHeader"]{
background:transparent !important;
}

[data-testid="stToolbar"]{
background:transparent !important;
}

[data-testid="stDecoration"]{
display:none !important;
}

[data-testid="stHeader"] button,
[data-testid="stToolbar"] button{
color:#dbeaff !important;
background:rgba(10,15,29,.92) !important;
border:1px solid rgba(76,145,255,.65) !important;
border-radius:9px !important;
box-shadow:0 0 18px rgba(58,116,255,.28) !important;
}

[data-testid="stSidebarCollapsedControl"]{
display:flex !important;
position:fixed !important;
top:.55rem !important;
left:.7rem !important;
z-index:100000 !important;
background:rgba(10,15,29,.92) !important;
border:1px solid rgba(76,145,255,.65) !important;
border-radius:9px !important;
box-shadow:0 0 18px rgba(58,116,255,.28) !important;
}


/* =====================================================
CONTAINER PRINCIPAL
===================================================== */

.block-container{
padding:1.25rem 1.6rem 2rem;
max-width:1700px;
}


/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"]{
background:
radial-gradient(
circle at 50% 12%,
rgba(50,117,255,.12),
transparent 25%
),
linear-gradient(
180deg,
#070a12 0%,
#080b14 100%
) !important;

border-right:1px solid rgba(76,122,255,.18);
}

section[data-testid="stSidebar"] > div{
padding-top:1.05rem;
}

.brand-small{
text-align:center;
font-family:Orbitron,sans-serif;
font-size:1.05rem;
font-weight:800;
letter-spacing:2px;
margin-top:-7px;
}

.brand-small span{
color:var(--cyan);
}

.side-caption{
text-align:center;
color:var(--muted);
font-size:.75rem;
margin-top:4px;
}

.nav-title{
color:#6fdbff;
font-size:.70rem;
font-weight:800;
letter-spacing:1.5px;
margin:25px 0 8px;
}

section[data-testid="stSidebar"] .stButton{
width:100% !important;
margin:0 0 10px !important;
}

section[data-testid="stSidebar"] .stButton > button{
width:100% !important;
min-height:58px !important;
padding:14px 16px !important;
justify-content:flex-start !important;
text-align:left !important;
border-radius:10px !important;
border:1px solid rgba(76,122,255,.24) !important;

background:
linear-gradient(
135deg,
rgba(16,22,37,.98),
rgba(10,14,25,.98)
) !important;

color:#dce6fa !important;
font-size:.92rem !important;
font-weight:750 !important;
box-shadow:none !important;
}

section[data-testid="stSidebar"] .stButton > button:hover{
border-color:rgba(0,210,255,.75) !important;
transform:translateX(3px) !important;
box-shadow:0 0 20px rgba(33,133,255,.20) !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"]{
background:
linear-gradient(
90deg,
rgba(21,116,255,.98),
rgba(112,49,235,.98)
) !important;

color:white !important;
border-color:rgba(138,201,255,.8) !important;
box-shadow:0 0 22px rgba(71,100,255,.30) !important;
}

.sidebar-status{
margin-top:55px;
padding:14px;
border:1px solid rgba(83,130,255,.20);
border-radius:12px;
background:rgba(10,14,25,.8);
}

.dot{
display:inline-block;
width:8px;
height:8px;
background:#20e889;
border-radius:50%;
box-shadow:0 0 10px #20e889;
margin-right:7px;
}


/* =====================================================
CABEÇALHO
===================================================== */

.top-title{
font-size:2.4rem;
font-weight:800;
margin:0;
}

.top-title span{
color:#39a7ff;
}

.top-subtitle{
color:#a0aabd;
font-size:1.05rem;
margin-top:4px;
}

.hero-line{
height:1px;
background:
linear-gradient(
90deg,
rgba(60,120,255,.55),
rgba(130,60,255,.32),
transparent
);

margin:22px 0 26px;
}


/* =====================================================
CONTROLES
===================================================== */

.top-controls{
display:flex;
align-items:flex-end;
}

.top-controls [data-testid="column"]{
display:flex;
flex-direction:column;
justify-content:flex-end;
}

.top-controls .stButton{
margin-top:0 !important;
}

.top-controls .stButton > button,
.top-controls .stDownloadButton > button{
min-height:42px !important;
height:42px !important;
margin-top:0 !important;
}

.top-controls div[data-baseweb="select"]{
min-height:42px !important;
}

.top-controls div[data-baseweb="select"] > div{
min-height:42px !important;
}


/* =====================================================
BOTÕES
===================================================== */

.stButton > button,
.stDownloadButton > button{
border-radius:10px !important;
border:1px solid rgba(68,137,255,.55) !important;

background:
linear-gradient(
100deg,
#0876df,
#5631d6
) !important;

color:#fff !important;
font-weight:700 !important;
min-height:42px !important;
box-shadow:0 0 18px rgba(47,128,255,.16);
transition:.2s ease !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover{
transform:translateY(-2px);
box-shadow:0 0 25px rgba(103,67,255,.35);
}


/* =====================================================
MÉTRICAS
===================================================== */

.metric-card{
position:relative;
overflow:hidden;
min-height:118px;
padding:18px;
border-radius:15px;
border:1px solid rgba(87,125,210,.22);

background:
linear-gradient(
145deg,
rgba(14,19,32,.97),
rgba(7,11,20,.92)
);

box-shadow:0 12px 35px rgba(0,0,0,.24);
transition:.25s ease;
}

.metric-card:hover{
transform:translateY(-2px);
border-color:rgba(70,157,255,.45);
box-shadow:0 16px 40px rgba(25,75,170,.18);
}

.metric-card:after{
content:"";
position:absolute;
width:115px;
height:115px;
right:-38px;
bottom:-48px;
border-radius:50%;

background:
radial-gradient(
circle,
rgba(37,131,255,.20),
transparent 70%
);
}

.metric-label{
color:#9ca8bc;
font-size:.78rem;
font-weight:700;
}

.metric-value{
font-family:Orbitron,sans-serif;
font-size:1.7rem;
font-weight:700;
margin-top:8px;
}

.metric-foot{
color:#718097;
font-size:.72rem;
margin-top:7px;
}

.icon-blue{
color:#4aa8ff;
}

.icon-purple{
color:#a871ff;
}

.icon-cyan{
color:#4de8ff;
}


/* =====================================================
PAINÉIS
===================================================== */

.panel{
border:1px solid rgba(88,130,230,.20);
background:
linear-gradient(
145deg,
rgba(11,16,28,.97),
rgba(6,10,18,.97)
);

border-radius:15px;
padding:16px;
box-shadow:0 15px 40px rgba(0,0,0,.22);
}

.panel-title{
font-size:1rem;
font-weight:800;
margin-bottom:4px;
}

.panel-sub{
color:#77849a;
font-size:.75rem;
}

.section-title{
font-size:1.22rem;
font-weight:800;
margin:5px 0 2px;
}

.section-subtitle{
color:#7d8ba2;
font-size:.78rem;
margin-bottom:12px;
}


/* =====================================================
CONTAINERS COM BORDA DO STREAMLIT
===================================================== */

div[data-testid="stVerticalBlockBorderWrapper"]{
background:
linear-gradient(
145deg,
rgba(11,16,28,.97),
rgba(6,10,18,.97)
) !important;

border:1px solid rgba(88,130,230,.20) !important;
border-radius:15px !important;
box-shadow:0 15px 40px rgba(0,0,0,.22) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div{
background:transparent !important;
}


/* =====================================================
RESUMO
===================================================== */

.summary-panel{
min-height:390px;
}

.summary-row{
display:flex;
justify-content:space-between;
gap:12px;
margin:12px 0;
color:#8290a7;
font-size:.8rem;
}

.summary-row b{
color:#f3f6ff;
}


/* =====================================================
SELECTBOX
===================================================== */

.stSelectbox label,
.stTextInput label{
color:#8cdfff !important;
font-weight:700 !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div{
background:#0c111e !important;
border-color:rgba(76,122,255,.25) !important;
}

div[data-baseweb="select"] span{
color:#e8efff !important;
}


/* =====================================================
TABELA
===================================================== */

.amira-table-wrap{
width:100%;
max-height:520px;
overflow:auto;

border:1px solid rgba(76,122,255,.25);
border-radius:12px;

background:#08101c;

box-shadow:
inset 0 0 25px rgba(22,78,160,.06),
0 10px 30px rgba(0,0,0,.18);
}

.amira-table{
width:100%;
border-collapse:separate;
border-spacing:0;

color:#e9f1ff;
font-size:.84rem;
}

.amira-table th{
position:sticky;
top:0;
z-index:2;

padding:12px 10px;
text-align:left;
font-weight:800;
color:#f4f7ff;

background:
linear-gradient(
135deg,
#101b2d,
#121a2c
);

border-bottom:1px solid rgba(76,145,255,.38);
white-space:nowrap;
}

.amira-table td{
padding:10px;

border-bottom:1px solid rgba(76,122,255,.14);

background:#0a1422;
color:#dbe6f8;

white-space:nowrap;
}

.amira-table tbody tr:nth-child(even) td{
background:#0c1727;
}

.amira-table tbody tr:hover td{
background:#10223a;
color:#ffffff;
}

.amira-table th:first-child{
border-top-left-radius:11px;
}

.amira-table th:last-child{
border-top-right-radius:11px;
}

.amira-table .num{
text-align:right;
}


/* =====================================================
FILTRO DE LOTE
===================================================== */

.lote-filter-info{
margin-top:8px;
padding:11px 14px;

border:1px solid rgba(32,232,137,.38);
border-radius:11px;

background:
linear-gradient(
90deg,
rgba(8,61,42,.58),
rgba(7,27,30,.70)
);

color:#bfe9d3;
font-size:.78rem;
}

.lote-filter-info b{
color:#37ef9b;
}

.lote-total{
color:#5bb0ff;
font-weight:800;
}

.lote-count{
color:#a875ff;
font-weight:800;
}


/* =====================================================
AVISO DE AUTOMAÇÃO
===================================================== */

.automation-note{
display:flex;
align-items:center;
gap:10px;

margin:18px 0 8px;
padding:13px 15px;

border:1px solid rgba(73,215,154,.25);
border-radius:11px;

background:
linear-gradient(
90deg,
rgba(19,66,55,.30),
rgba(12,22,38,.65)
);

color:#b8c8da;
font-size:.80rem;
}

.automation-note b{
color:#53efa5;
}


/* =====================================================
EXPANDER
===================================================== */

[data-testid="stExpander"]{
border:1px solid rgba(83,130,255,.25) !important;
border-radius:11px !important;
background:rgba(10,15,27,.70) !important;
margin-bottom:9px !important;
}

[data-testid="stExpander"] summary{
font-weight:750 !important;
color:#e9f1ff !important;
}


/* =====================================================
RODAPÉ
===================================================== */

.footer{
color:#59677d;
font-size:.68rem;
text-align:center;
padding:20px 0 0;
}

.small-note{
color:#6f7e96;
font-size:.72rem;
}


/* =====================================================
PLOTLY
===================================================== */

/*
Impede qualquer fundo branco ao redor dos gráficos.
*/

.js-plotly-plot,
.plotly,
.plot-container{
background:transparent !important;
}

.js-plotly-plot .main-svg{
background:transparent !important;
}


/* =====================================================
RESPONSIVIDADE
===================================================== */

@media (max-width:900px){

.block-container{
padding:1rem .8rem 2rem;
}

.top-title{
font-size:1.8rem;
}

.top-subtitle{
font-size:.9rem;
}

.metric-value{
font-size:1.35rem;
}
}

</style>
""",
unsafe_allow_html=True,
)


# =========================================================
# FUNÇÕES DE DADOS
# =========================================================

def vazio():
return pd.DataFrame(
columns=[
"Data",
"Hora",
"Peso (kg)",
"Lote"
]
)


def formatar_data_planilha(valor):

if pd.isna(valor) or str(valor).strip() == "":
return None

texto = str(valor).strip()

try:

data = pd.to_datetime(
texto,
format="%d/%m/%Y",
errors="coerce"
)

if not pd.isna(data):
return data.strftime("%d/%m/%Y")

except (TypeError, ValueError):
pass

try:

if "T" in texto or texto.endswith("Z"):

data = pd.to_datetime(
texto,
utc=True,
errors="coerce"
)

if not pd.isna(data):

return data.tz_convert(
TZ
).strftime("%d/%m/%Y")

data = pd.to_datetime(
texto,
errors="coerce",
dayfirst=True
)

if not pd.isna(data):
return data.strftime("%d/%m/%Y")

except (TypeError, ValueError):
pass

return texto


def formatar_hora_planilha(valor):

if pd.isna(valor) or str(valor).strip() == "":
return None

texto = str(valor).strip()

hora = re.match(
r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$",
texto
)

if hora:

horas = int(hora.group(1))
minutos = hora.group(2)
segundos = hora.group(3) or "00"

return (
f"{horas:02d}:"
f"{minutos}:"
f"{segundos}"
)

marco_excel = re.match(
r"^1899-12-\d{2}T(\d{2}:\d{2}:\d{2})",
texto
)

if marco_excel:
return marco_excel.group(1)

try:

if "T" in texto or texto.endswith("Z"):

data = pd.to_datetime(
texto,
utc=True,
errors="coerce"
)

if not pd.isna(data):

return data.tz_convert(
TZ
).strftime("%H:%M:%S")

except (TypeError, ValueError):
pass

return texto


def normalizar_lote(valor):

if pd.isna(valor):
return "Sem lote"

texto = str(valor).strip()

if not texto:
return "Sem lote"

texto = re.sub(
r"\s+",
" ",
texto
)

if re.fullmatch(
r"\d+\.0+",
texto
):
texto = texto.split(".")[0]

return texto


def normalizar_colunas(df):

if df is None or df.empty:
return vazio()

df = df.copy()

renomear = {}

for c in df.columns:

chave = (
str(c)
.strip()
.lower()
.replace(" ", "")
.replace("_", "")
)

if chave in {
"peso",
"peso(kg)",
"pesokg"
}:

renomear[c] = "Peso (kg)"

elif chave == "data":

renomear[c] = "Data"

elif chave == "hora":

renomear[c] = "Hora"

elif chave == "lote":

renomear[c] = "Lote"

df = df.rename(
columns=renomear
)

for col in [
"Data",
"Hora",
"Peso (kg)",
"Lote"
]:

if col not in df.columns:
df[col] = None

df["Peso (kg)"] = pd.to_numeric(
df["Peso (kg)"],
errors="coerce"
)

df["Data"] = df["Data"].map(
formatar_data_planilha
)

df["Hora"] = df["Hora"].map(
formatar_hora_planilha
)

df["Lote"] = df["Lote"].map(
normalizar_lote
)

return (
df[
[
"Data",
"Hora",
"Peso (kg)",
"Lote"
]
]
.dropna(
subset=["Peso (kg)"],
how="all"
)
.reset_index(drop=True)
)


@st.cache_data(ttl=15)
def carregar_dados_todas_abas():

resposta = requests.get(
URL_SCRIPT,
timeout=20
)

resposta.raise_for_status()

dados = resposta.json()

if not isinstance(dados, dict):

raise ValueError(
"O Google Apps Script não devolveu "
"um JSON de abas."
)

resultado = {}

for nome_aba, conteudo in dados.items():

if (
not isinstance(conteudo, list)
or not conteudo
):
continue

cabecalho = conteudo[0]
linhas = conteudo[1:]

if not isinstance(
cabecalho,
list
):
continue

resultado[str(nome_aba)] = (
normalizar_colunas(
pd.DataFrame(
linhas,
columns=cabecalho
)
)
)

return resultado


def chave_aba(nome):

data = data_da_aba(nome)

return (
datetime.combine(
data,
datetime.min.time()
)
if data
else datetime.min
)


def data_da_aba(nome):

texto = str(nome)

for padrao, formato in [

(
r"(?<!\d)(\d{2}-\d{2}-\d{4})(?!\d)",
"%d-%m-%Y"
),

(
r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)",
"%Y-%m-%d"
)

]:

encontrado = re.search(
padrao,
texto
)

if encontrado:

try:

return datetime.strptime(
encontrado.group(1),
formato
).date()

except ValueError:
pass

return None


def rotulo_aba(nome):

data = data_da_aba(nome)

return (
data.strftime("%d/%m/%Y")
if data
else str(nome)
)


def formatar_numero(valor):

return (
f"{valor:,.2f}"
.replace(",", "X")
.replace(".", ",")
.replace("X", ".")
)


# =========================================================
# TABELA AMIRA
# =========================================================

def tabela_amira(
df,
numero=True,
max_height=520
):

if df is None or df.empty:

st.info(
"Nenhum registro para exibir."
)

return

tabela = df.copy()

html = f"""
<div class="amira-table-wrap"
style="max-height:{max_height}px;">

<table class="amira-table">

<thead>
<tr>
"""

for coluna in tabela.columns:

classe = (
"num"
if numero and coluna == "Peso (kg)"
else ""
)

html += (
f'<th class="{classe}">'
f'{coluna}'
f'</th>'
)

html += """
</tr>
</thead>

<tbody>
"""

for _, linha in tabela.iterrows():

html += "<tr>"

for coluna in tabela.columns:

valor = linha[coluna]

if pd.isna(valor):

valor = ""

elif coluna in {
"Peso (kg)",
"Peso total (kg)",
"Média (kg)"
}:

try:

valor = formatar_numero(
float(valor)
)

except (
TypeError,
ValueError
):

valor = str(valor)

else:

valor = str(valor)

classe = (
"num"
if numero
and coluna in {
"Peso (kg)",
"Peso total (kg)",
"Média (kg)"
}
else ""
)

html += (
f'<td class="{classe}">'
f'{valor}'
f'</td>'
)

html += "</tr>"

html += """
</tbody>

</table>

</div>
"""

st.markdown(
html,
unsafe_allow_html=True
)


# =========================================================
# XLSX
# =========================================================

def gerar_xlsx(df):

buffer = io.BytesIO()

try:

from openpyxl import Workbook
from openpyxl.styles import (
Font,
PatternFill
)

wb = Workbook()

ws = wb.active
ws.title = "Registros"

cab = list(df.columns)

ws.append(cab)

for cell in ws[1]:

cell.font = Font(
bold=True,
color="FFFFFF"
)

cell.fill = PatternFill(
"solid",
fgColor="111827"
)

for row in df.itertuples(
index=False,
name=None
):

ws.append(
list(row)
)

ws.freeze_panes = "A2"
ws.auto_filter.ref = ws.dimensions

for col in ws.columns:

letra = col[0].column_letter

maior = max(
len(str(c.value or ""))
for c in col
)

ws.column_dimensions[
letra
].width = min(
max(maior + 2, 12),
28
)

wb.save(buffer)

return buffer.getvalue()

except Exception:

return df.to_csv(
index=False,
sep=";"
).encode(
"utf-8-sig"
)


# =========================================================
# GRÁFICOS
# =========================================================

def grafico_layout(
fig,
height=300,
showlegend=False
):

fig.update_layout(

template="plotly_dark",

paper_bgcolor="rgba(0,0,0,0)",
plot_bgcolor="rgba(0,0,0,0)",

font=dict(
color="#aeb9cb",
family="Inter"
),

margin=dict(
l=15,
r=15,
t=25,
b=35
),

height=height,

showlegend=showlegend,

hoverlabel=dict(
bgcolor="#101827",
bordercolor="#2f80ff",
font=dict(
color="#ffffff",
family="Inter"
)
),

xaxis=dict(

gridcolor="rgba(90,120,180,.10)",

zeroline=False,

linecolor="rgba(90,120,180,.18)",

tickfont=dict(
color="#8f9bb2"
),

title_font=dict(
color="#aeb9cb"
)
),

yaxis=dict(

gridcolor="rgba(90,120,180,.10)",

zeroline=False,

linecolor="rgba(90,120,180,.18)",

tickfont=dict(
color="#8f9bb2"
),

title_font=dict(
color="#aeb9cb"
)
)
)

return fig


def grafico_barra(
df,
x,
y,
cor,
titulo_y=None,
altura=300,
texto=False
):

fig = px.bar(
df,
x=x,
y=y
)

fig.update_traces(
marker_color=cor,
marker_line_width=0
)

if texto:

fig.update_traces(
texttemplate="%{y:.2f}",
textposition="outside",
cliponaxis=False
)

fig.update_layout(
xaxis_title=None,
yaxis_title=titulo_y
)

return grafico_layout(
fig,
height=altura
)


# =========================================================
# MÉTRICAS
# =========================================================

def mostrar_metricas(df):

total_caixas = len(df)

peso_total = (
float(
df["Peso (kg)"].sum()
)
if not df.empty
else 0
)

media = (
float(
df["Peso (kg)"].mean()
)
if not df.empty
else 0
)

cards = [

(
"📦",
"Caixas Passadas",
f"{total_caixas}",
"Registros filtrados",
"cyan"
),

(
"⚖",
"Peso Total (kg)",
formatar_numero(
peso_total
),
"Peso acumulado",
"blue"
),

(
"◈",
"Média por Caixa",
f"{formatar_numero(media)} kg",
"Média dos registros",
"purple"
)

]

cols = st.columns(3)

for col, (
icon,
label,
value,
foot,
color
) in zip(cols, cards):

with col:

st.markdown(
f"""
<div class="metric-card">

<div class="metric-label">
<span class="icon-{color}">
{icon}
</span>

&nbsp;&nbsp;{label}
</div>

<div class="metric-value">
{value}
</div>

<div class="metric-foot">
{foot}
</div>

</div>
""",
unsafe_allow_html=True
)


def resumo_dia(df):

peso_total = (
float(
df["Peso (kg)"].sum()
)
if not df.empty
else 0
)

media = (
float(
df["Peso (kg)"].mean()
)
if not df.empty
else 0
)

total_caixas = len(df)

return (
peso_total,
media,
total_caixas
)


# =========================================================
# AGRUPAMENTO POR LOTE
# =========================================================

def agrupar_por_lote(df):

if df is None or df.empty:

return pd.DataFrame(
columns=[
"Lote",
"Pesagens",
"Peso total (kg)",
"Média (kg)"
]
)

trabalho = df.copy()

trabalho["Lote"] = (
trabalho["Lote"]
.map(normalizar_lote)
)

agrupado = (
trabalho
.groupby(
"Lote",
dropna=False
)
.agg(

Pesagens=(
"Peso (kg)",
"count"
),

**{
"Peso total (kg)": (
"Peso (kg)",
"sum"
),

"Média (kg)": (
"Peso (kg)",
"mean"
)
}

)
.reset_index()
)

def ordem_lote(valor):

texto = str(valor)

if texto.isdigit():

return (
0,
int(texto)
)

return (
1,
texto.lower()
)

agrupado["_ordem"] = (
agrupado["Lote"]
.map(ordem_lote)
)

agrupado = (
agrupado
.sort_values("_ordem")
.drop(columns="_ordem")
.reset_index(drop=True)
)

return agrupado


# =========================================================
# PRODUÇÃO POR LOTE
# =========================================================

def mostrar_producao_por_lote(df):

agrupado = agrupar_por_lote(df)

st.markdown(
"""
<div class="section-title">
📦 Produção por Lote
</div>

<div class="section-subtitle">
O sistema agrupa automaticamente todas as
pesagens que possuem o mesmo lote.
</div>
""",
unsafe_allow_html=True
)

if agrupado.empty:

st.info(
"Não há lotes para agrupar."
)

return

tabela = agrupado.copy()

tabela[
"Peso total (kg)"
] = tabela[
"Peso total (kg)"
].round(2)

tabela[
"Média (kg)"
] = tabela[
"Média (kg)"
].round(2)

tabela[
"Pesagens"
] = tabela[
"Pesagens"
].astype(int)

tabela_exibicao = tabela.copy()

# =====================================================
# PAINEL DA TABELA
# =====================================================

col_tabela, col_graficos = st.columns(
[1.05, 1.25],
gap="large"
)

with col_tabela:

with st.container(border=True):

st.markdown(
"""
<div class="panel-title">
📋 Resumo dos Lotes
</div>

<div class="panel-sub">
Total acumulado por lote
</div>
""",
unsafe_allow_html=True
)

tabela_amira(
tabela_exibicao,
max_height=360
)

# =====================================================
# GRÁFICOS
# =====================================================

with col_graficos:

with st.container(border=True):

st.markdown(
"""
<div class="panel-title">
⚖ Peso total por lote
</div>

<div class="panel-sub">
Peso acumulado de cada lote
</div>
""",
unsafe_allow_html=True
)

fig_peso = px.bar(
agrupado,
x="Lote",
y="Peso total (kg)"
)

fig_peso.update_traces(
marker_color="#2f80ff",
marker_line_width=0,
hovertemplate=(
"<b>Lote %{x}</b><br>"
"Peso: %{y:.2f} kg"
"<extra></extra>"
)
)

fig_peso.update_layout(
xaxis_title="Lote",
yaxis_title="Peso (kg)"
)

st.plotly_chart(
grafico_layout(
fig_peso,
height=285
),
use_container_width=True,
config={
"displayModeBar": False,
"responsive": True
}
)

st.markdown(
"""
<div class="panel-title"
style="margin-top:8px;">
📦 Pesagens por lote
</div>

<div class="panel-sub">
Quantidade de registros em cada lote
</div>
""",
unsafe_allow_html=True
)

fig_qtd = px.bar(
agrupado,
x="Lote",
y="Pesagens"
)

fig_qtd.update_traces(
marker_color="#8a35ff",
marker_line_width=0,
hovertemplate=(
"<b>Lote %{x}</b><br>"
"Pesagens: %{y}"
"<extra></extra>"
)
)

fig_qtd.update_layout(
xaxis_title="Lote",
yaxis_title="Quantidade"
)

st.plotly_chart(
grafico_layout(
fig_qtd,
height=250
),
use_container_width=True,
config={
"displayModeBar": False,
"responsive": True
}
)


# =========================================================
# CARREGAMENTO GLOBAL
# =========================================================

try:

dados_abas = (
carregar_dados_todas_abas()
)

erro_api = None

except Exception as erro:

dados_abas = {}
erro_api = str(erro)


lista_abas = sorted(
dados_abas.keys(),
key=chave_aba,
reverse=True
)


# =========================================================
# ESTADO
# =========================================================

dia_atual = st.session_state.get(
"dia_selecionado",
lista_abas[0]
if lista_abas
else None
)

if (
dia_atual not in lista_abas
and lista_abas
):

dia_atual = lista_abas[0]


lote_atual = st.session_state.get(
"lote_selecionado",
"Todos os lotes"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

if os.path.exists("logo.png"):

st.image(
"logo.png",
use_container_width=True
)

elif os.path.exists("logo.jpg"):

st.image(
"logo.jpg",
use_container_width=True
)

st.markdown(
"""
<div class="brand-small">
Sistema <span>AMIRA</span>
</div>

<div class="side-caption">
Monitoramento • Automação • Precisão
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="nav-title">
MENU DE NAVEGAÇÃO
</div>
""",
unsafe_allow_html=True
)

opcoes_menu = [
"📋 Registro e Dados",
"📊 Gráficos e Análises",
"🗂 Histórico de Planilhas"
]

menu = st.session_state.get(
"menu_amira",
opcoes_menu[0]
)

for indice, opcao in enumerate(
opcoes_menu
):

if st.button(
opcao,
key=f"menu_amira_{indice}",
type=(
"primary"
if menu == opcao
else "secondary"
),
use_container_width=True
):

st.session_state[
"menu_amira"
] = opcao

st.rerun()

st.markdown(
"""
<div class="sidebar-status">

<div style="font-weight:800;">
Sistema AMIRA
</div>

<div style="
color:#7f8da4;
font-size:.75rem;
margin-top:5px;
">

<span class="dot"></span>
Monitoramento ativo

</div>

</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="footer">
©️ 2026 AMIRA • SENAI<br>
IoT • Automação • Precisão
</div>
""",
unsafe_allow_html=True
)


# =========================================================
# CABEÇALHO
# =========================================================

if menu == "📋 Registro e Dados":

st.markdown(
"""
<div class="top-title">
Bem-vindo à <span>AMIRA</span>
</div>

<div class="top-subtitle">
Sistema de Monitoramento e Registro de Produção
</div>
""",
unsafe_allow_html=True
)

elif menu == "📊 Gráficos e Análises":

st.markdown(
"""
<div class="top-title">
<span>Gráficos</span> e Análises
</div>

<div class="top-subtitle">
Explore o histórico e compare dias e meses
de produção.
</div>
""",
unsafe_allow_html=True
)

else:

st.markdown(
"""
<div class="top-title">
<span>Histórico</span> de Planilhas
</div>

<div class="top-subtitle">
Controle de lançamentos no sistema da empresa.
</div>
""",
unsafe_allow_html=True
)


st.markdown(
"<div style='margin-top:15px;'></div>",
unsafe_allow_html=True
)


# =========================================================
# CONTROLES SUPERIORES
# =========================================================

st.markdown(
'<div class="top-controls">',
unsafe_allow_html=True
)

col_dia, col_lote, col_b1, col_b2 = st.columns(
[1.25, 1.25, 0.9, 0.9],
gap="small"
)


# =========================================================
# DIA
# =========================================================

with col_dia:

if (
menu == "📋 Registro e Dados"
and lista_abas
):

dia_selecionado_novo = st.selectbox(
"📅 Dia de Produção",
options=lista_abas,
format_func=rotulo_aba,
index=(
lista_abas.index(
dia_atual
)
if dia_atual in lista_abas
else 0
),
key="select_dia_amira"
)

if (
dia_selecionado_novo
!= dia_atual
):

st.session_state[
"dia_selecionado"
] = dia_selecionado_novo

st.session_state[
"lote_selecionado"
] = "Todos os lotes"

st.rerun()

dia_atual = (
dia_selecionado_novo
)


# =========================================================
# DADOS DO DIA
# =========================================================

df = (
dados_abas.get(
dia_atual,
vazio()
)
if dia_atual
else vazio()
)


# =========================================================
# FILTRO DE LOTE
# =========================================================

with col_lote:

if (
menu == "📋 Registro e Dados"
and not df.empty
):

lotes_disponiveis = sorted(

df["Lote"]
.map(normalizar_lote)
.drop_duplicates()
.tolist(),

key=lambda x: (
(0, int(x))
if str(x).isdigit()
else (1, str(x).lower())
)
)

opcoes_lote = [
"Todos os lotes"
] + lotes_disponiveis

if lote_atual not in opcoes_lote:

lote_atual = (
"Todos os lotes"
)

lote_selecionado_novo = (
st.selectbox(
"🔎 Filtrar por lote",
options=opcoes_lote,
index=opcoes_lote.index(
lote_atual
),
key="select_lote_amira"
)
)

if (
lote_selecionado_novo
!= lote_atual
):

st.session_state[
"lote_selecionado"
] = lote_selecionado_novo

st.rerun()

lote_atual = (
lote_selecionado_novo
)

elif menu != "📋 Registro e Dados":

st.empty()


# =========================================================
# APLICA FILTRO
# =========================================================

if (
menu == "📋 Registro e Dados"
and lote_atual != "Todos os lotes"
):

df_filtrado = df[
df["Lote"].map(
normalizar_lote
) == lote_atual
].copy()

else:

df_filtrado = df.copy()


# =========================================================
# RECARREGAR
# =========================================================

with col_b1:

if menu == "📋 Registro e Dados":

if st.button(
"🔄 Recarregar Dados",
use_container_width=True,
key="recarregar_amira"
):

carregar_dados_todas_abas.clear()

st.rerun()


# =========================================================
# DOWNLOAD
# =========================================================

with col_b2:

if (
menu == "📋 Registro e Dados"
and dia_atual
and not df_filtrado.empty
):

st.download_button(
label="⬇️ Baixar Planilha",
data=gerar_xlsx(
df_filtrado
),
file_name=(
"AMIRA_Producao_"
f"{rotulo_aba(dia_atual).replace('/', '-')}"
f"{('_Lote_' + str(lote_atual)) if lote_atual != 'Todos os lotes' else ''}"
".xlsx"
),
mime=(
"application/vnd.openxmlformats-officedocument."
"spreadsheetml.sheet"
),
use_container_width=True,
key="download_amira"
)


st.markdown(
"</div>",
unsafe_allow_html=True
)

st.markdown(
"<div class='hero-line'></div>",
unsafe_allow_html=True
)


# =========================================================
# 1. REGISTRO E DADOS
# =========================================================

if menu == "📋 Registro e Dados":

if (
lote_atual != "Todos os lotes"
and not df_filtrado.empty
):

st.markdown(
f"""
<div class="lote-filter-info">
🔎 Filtro ativo:
<b>Lote {lote_atual}</b>
• Exibindo apenas as pesagens desse lote.
</div>
""",
unsafe_allow_html=True
)

elif not df.empty:

st.markdown(
"""
<div class="lote-filter-info">
🟢 <b>Todos os lotes</b>
• O sistema agrupou automaticamente
os registros iguais.
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="section-title">
Dados do Dia
</div>
""",
unsafe_allow_html=True
)

mostrar_metricas(
df_filtrado
)

st.markdown(
"<br>",
unsafe_allow_html=True
)


# =====================================================
# PRODUÇÃO POR LOTE
# =====================================================

mostrar_producao_por_lote(
df_filtrado
)

st.markdown(
"<br>",
unsafe_allow_html=True
)


# =====================================================
# REGISTROS
# =====================================================

st.markdown(
"""
<div class="section-title"
style="font-size:1.2rem;">
📋 Registros de Produção
</div>

<div class="section-subtitle">
Pesagens registradas no dia selecionado.
</div>
""",
unsafe_allow_html=True
)

if df_filtrado.empty:

st.info(
"Aguardando pesagens para exibir na tabela."
)

else:

tabela_exibicao = (
df_filtrado
.copy()
.reset_index(drop=True)
)

tabela_exibicao.insert(
0,
"#",
tabela_exibicao.index + 1
)

tabela_amira(
tabela_exibicao,
max_height=440
)


# =====================================================
# RESUMO
# =====================================================

st.markdown(
"<br>",
unsafe_allow_html=True
)

peso_total, media, total_caixas = (
resumo_dia(
df_filtrado
)
)

with st.container(border=True):

st.markdown(
"""
<div class="panel-title">
Resumo do Dia
</div>

<div class="panel-sub">
Indicadores principais
</div>
""",
unsafe_allow_html=True
)

st.markdown(
f"""
<div style="
display:flex;
justify-content:center;
align-items:center;
padding:30px 0 25px;
">

<div style="
width:145px;
height:145px;
border-radius:50%;

background:
conic-gradient(
#3d8cff 85%,
rgba(255,255,255,0.05) 85%
);

display:flex;
justify-content:center;
align-items:center;

box-shadow:
0 0 20px
rgba(61,140,255,0.15);
">

<div style="
width:125px;
height:125px;
border-radius:50%;
background:#080c14;

display:flex;
flex-direction:column;
justify-content:center;
align-items:center;

border:1px solid
rgba(88,130,230,.15);
">

<span style="
font-family:'Orbitron',sans-serif;
font-size:1.35rem;
font-weight:800;
color:#fff;
">
{formatar_numero(peso_total)}
</span>

<span style="
font-size:0.75rem;
color:#77849a;
margin-top:2px;
">
kg
</span>

</div>

</div>

</div>

<div class="summary-row">
<span>📦 Caixas passadas</span>
<b>{total_caixas}</b>
</div>

<div class="summary-row">
<span>↗️ Média por caixa</span>
<b>{formatar_numero(media)} kg</b>
</div>

<div class="summary-row">
<span>⚖ Peso total acumulado</span>
<b>{formatar_numero(peso_total)} kg</b>
</div>
""",
unsafe_allow_html=True
)


# =====================================================
# DESEMPENHO
# =====================================================

st.markdown(
"""
<br>

<div class="section-title"
style="font-size:1.2rem;">
Desempenho do Dia
</div>
""",
unsafe_allow_html=True
)

g1, g2 = st.columns(
2,
gap="large"
)


# =====================================================
# PESO AO LONGO DO DIA
# =====================================================

with g1:

with st.container(border=True):

st.markdown(
"""
<div class="panel-title">
📈 Peso ao longo do dia
</div>

<div class="panel-sub">
Evolução das pesagens registradas
</div>
""",
unsafe_allow_html=True
)

if not df_filtrado.empty:

dfg = (
df_filtrado
.reset_index(drop=True)
.copy()
)

dfg["Registro"] = (
dfg.index + 1
)

fig = px.area(
dfg,
x="Registro",
y="Peso (kg)"
)

fig.update_traces(
line_color="#3d8cff",
fillcolor=(
"rgba(61,140,255,.15)"
),
hovertemplate=(
"<b>Registro %{x}</b><br>"
"Peso: %{y:.2f} kg"
"<extra></extra>"
)
)

st.plotly_chart(
grafico_layout(
fig,
height=310
),
use_container_width=True,
config={
"displayModeBar": False,
"responsive": True
}
)

else:

st.info(
"Sem dados para gerar o gráfico."
)


# =====================================================
# DISTRIBUIÇÃO
# =====================================================

with g2:

with st.container(border=True):

st.markdown(
"""
<div class="panel-title">
📊 Distribuição dos pesos
</div>

<div class="panel-sub">
Distribuição das pesagens registradas
</div>
""",
unsafe_allow_html=True
)

if not df_filtrado.empty:

fig2 = px.histogram(
df_filtrado,
x="Peso (kg)",
nbins=8
)

fig2.update_traces(
marker_color="#8a35ff",
marker_line_color="#05070d",
marker_line_width=1,

hovertemplate=(
"Peso: %{x:.2f} kg<br>"
"Quantidade: %{y}"
"<extra></extra>"
)
)

fig2.update_layout(
bargap=0.08,
xaxis_title="Peso (kg)",
yaxis_title="Quantidade"
)

st.plotly_chart(
grafico_layout(
fig2,
height=310
),
use_container_width=True,
config={
"displayModeBar": False,
"responsive": True
}
)

else:

st.info(
"Sem dados para gerar o gráfico."
)


# =========================================================
# 2. GRÁFICOS E ANÁLISES
# =========================================================

elif menu == "📊 Gráficos e Análises":

if not lista_abas:

st.info(
"Aguardando registros para gerar as análises."
)

else:

st.markdown(
"""
<div class="panel-title"
style="
font-size:1.15rem;
color:#00d2ff;
">
Comparativo Diário
</div>

<div class="section-subtitle">
Produção dia a dia
</div>
""",
unsafe_allow_html=True
)

resumo = []

for nome, temp in dados_abas.items():

if not temp.empty:

resumo.append(
{
"Data": rotulo_aba(nome),

"Peso total (kg)": temp[
"Peso (kg)"
].sum(),

"Caixas": len(temp)
}
)

rdf = pd.DataFrame(
resumo
)

if not rdf.empty:

c3, c4 = st.columns(
2,
gap="large"
)


# =================================================
# PESO DIÁRIO
# =================================================

with c3:

with st.container(border=True):

st.markdown(
"""
<div class="panel-title">
⚖ Peso Diário (kg)
</div>

<div class="panel-sub">
Peso total produzido por dia
</div>
""",
unsafe_allow_html=True
)

fig = px.bar(
rdf,
x="Data",
y="Peso total (kg)"
)

fig.update_traces(
marker_color="#2f80ff",
marker_line_width=0,

hovertemplate=(
"<b>%{x}</b><br>"
"Peso: %{y:.2f} kg"
"<extra></extra>"
)
)

st.plotly_chart(
grafico_layout(
fig,
height=320
),
use_container_width=True,
config={
"displayModeBar": False,
"responsive": True
}
)


# =================================================
# CAIXAS POR DIA
# =================================================

with c4:

with st.container(border=True):

st.markdown(
"""
<div class="panel-title">
📦 Caixas por Dia
</div>

<div class="panel-sub">
Quantidade de caixas registradas
</div>
""",
unsafe_allow_html=True
)

fig = px.bar(
rdf,
x="Data",
y="Caixas"
)

fig.update_traces(
marker_color="#8a35ff",
marker_line_width=0,

hovertemplate=(
"<b>%{x}</b><br>"
"Caixas: %{y}"
"<extra></extra>"
)
)

st.plotly_chart(
grafico_layout(
fig,
height=320
),
use_container_width=True,
config={
"displayModeBar": False,
"responsive": True
}
)


# =====================================================
# ANÁLISE MENSAL
# =====================================================

st.markdown(
"""
<br>

<div class="panel-title"
style="
font-size:1.15rem;
color:#00d2ff;
">
Análise de Longo Prazo (Mensal)
</div>

<div class="section-subtitle">
Comparativo histórico agrupado por mês e ano
para controle gerencial.
</div>
""",
unsafe_allow_html=True
)

long_term_data = []

for nome, temp in dados_abas.items():

if not temp.empty:

dt = data_da_aba(nome)

if dt:

long_term_data.append(
{
"Ano": str(dt.year),

"Mês_Num": dt.month,

"Mês/Ano":
f"{dt.month:02d}/{dt.year}",

"Peso total (kg)": temp[
"Peso (kg)"
].sum(),

"Caixas": len(temp)
}
)

if long_term_data:

df_lt = pd.DataFrame(
long_term_data
)

df_grp = (
df_lt
.groupby(
[
"Ano",
"Mês_Num",
"Mês/Ano"
]
)
.sum(
numeric_only=True
)
.reset_index()
.sort_values(
by=[
"Ano",
"Mês_Num"
]
)
)


# =================================================
# GRÁFICO MENSAL DE PESO
# =================================================

lt1, lt2 = st.columns(
2,
gap="large"
)

with lt1:

with st.container(
border=True
):

st.markdown(
"""
<div class="panel-title">
⚖ Produção Mensal Acumulada
</div>

<div class="panel-sub">
Peso total produzido por mês
</div>
""",
unsafe_allow_html=True
)

fig_lt1 = px.bar(
df_grp,
x="Mês/Ano",
y="Peso total (kg)",
color="Ano",
color_discrete_sequence=[
"#00d2ff",
"#2f80ff",
"#8a35ff"
]
)

fig_lt1.update_traces(
marker_line_width=0,

hovertemplate=(
"<b>%{x}</b><br>"
"Peso: %{y:.2f} kg"
"<extra></extra>"
)
)

fig_lt1.update_layout(
xaxis_title="Mês/Ano",
yaxis_title="Peso (kg)",
legend_title="Ano"
)

st.plotly_chart(
grafico_layout(
fig_lt1,
height=320,
showlegend=True
),
use_container_width=True,
config={
"displayModeBar": False,
"responsive": True
}
)


# =================================================
# GRÁFICO MENSAL DE CAIXAS
# =================================================

with lt2:

with st.container(
border=True
):

st.markdown(
"""
<div class="panel-title">
📦 Volume Mensal
</div>

<div class="panel-sub">
Quantidade de caixas por mês
</div>
""",
unsafe_allow_html=True
)

fig_lt2 = px.line(
df_grp,
x="Mês/Ano",
y="Caixas",
color="Ano",
markers=True,
color_discrete_sequence=[
"#00d2ff",
"#2f80ff",
"#8a35ff"
]
)

fig_lt2.update_traces(
line_width=3,
marker=dict(
size=8
),

hovertemplate=(
"<b>%{x}</b><br>"
"Caixas: %{y}"
"<extra></extra>"
)
)

fig_lt2.update_layout(
xaxis_title="Mês/Ano",
yaxis_title="Quantidade",
legend_title="Ano"
)

st.plotly_chart(
grafico_layout(
fig_lt2,
height=320,
showlegend=True
),
use_container_width=True,
config={
"displayModeBar": False,
"responsive": True
}
)

else:

st.info(
"Aguardando dados históricos suficientes "
"para gerar gráficos mensais."
)


# =========================================================
# 3. HISTÓRICO DE PLANILHAS
# =========================================================

else:

if "planilhas_lancadas" not in st.session_state:

st.session_state[
"planilhas_lancadas"
] = set()

if not lista_abas:

st.info(
"Ainda não há planilhas registradas pela balança."
)

else:

for nome in sorted(
lista_abas,
key=chave_aba,
reverse=True
):

temp = dados_abas.get(
nome,
vazio()
)

rotulo = rotulo_aba(
nome
)

esta_lancada = (
nome
in st.session_state[
"planilhas_lancadas"
]
)

if esta_lancada:

titulo = (
f"🟢 {rotulo}"
" • ✓ Lançado no sistema"
)

else:

titulo = (
f"🟠 {rotulo}"
" • ! Pendente de lançamento"
)

with st.expander(
titulo,
expanded=False
):

if not esta_lancada:

st.warning(
"⚠️ Esta planilha ainda não foi "
"marcada como lançada no sistema oficial."
)

if st.button(
f"✓ Confirmar Lançamento — {rotulo}",
key=f"btn_{nome}",
type="primary"
):

st.session_state[
"planilhas_lancadas"
].add(nome)

st.rerun()

else:

st.success(
"✅ Lançamento confirmado pela equipe!"
)

if temp.empty:

st.info(
"A planilha existe, mas ainda "
"não possui registros."
)

else:

tabela_historico = (
temp
.copy()
.reset_index(drop=True)
)

tabela_historico.insert(
0,
"#",
tabela_historico.index + 1
)

tabela_amira(
tabela_historico,
max_height=430
)

# =========================================
# RESUMO DOS LOTES
# =========================================

agrupado_historico = (
agrupar_por_lote(
temp
)
)

if not agrupado_historico.empty:

st.markdown(
"""
<div class="panel-title"
style="margin-top:18px;">
📦 Resumo por lote
</div>
""",
unsafe_allow_html=True
)

resumo_historico = (
agrupado_historico.copy()
)

tabela_amira(
resumo_historico,
max_height=300
)


# =========================================================
# RODAPÉ
# =========================================================

st.markdown(
"""
<div class="footer">
AMIRA • Sistema de Monitoramento e Registro de Produção
• SENAI
</div>
""",
unsafe_allow_html=True
)
