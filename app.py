from pathlib import Path

code = r'''import io, os, re

from datetime import datetime

import pandas as pd

import plotly.express as px

import requests

import streamlit as st

st.set_page_config(page_title="AMIRA | Monitoramento de Produção", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

URL_SCRIPT = "https://script.google.com/macros/s/AKfycbwQ8IIVRIDsx8-CdJeKw6LUr4rBOFGX0jb42augc8v89TZVNWy0O8mlBAK23O2Tjymmaw/exec"

TZ = "America/Sao_Paulo"

st.markdown("""<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@600;700;800&display=swap');

:root{--bg:#05070d;--panel:#0b0f1a;--line:rgba(85,139,255,.24);--blue:#2f80ff;--cyan:#00d2ff;--purple:#8a35ff;--green:#20e889;--text:#f4f7ff;--muted:#8f9bb2}

html,body,[class*="css"]{font-family:Inter,sans-serif}.stApp{background:radial-gradient(circle at 68% 12%,rgba(54,83,180,.13),transparent 28%),radial-gradient(circle at 96% 76%,rgba(138,53,255,.12),transparent 31%),#05070d;color:var(--text)}

header[data-testid="stHeader"]{background:transparent!important}[data-testid="stToolbar"]{display:flex!important;background:transparent!important}[data-testid="stDecoration"]{display:none!important}

[data-testid="stHeader"] button,[data-testid="stToolbar"] button,[data-testid="stSidebarCollapsedControl"]{color:#dbeaff!important;background:rgba(10,15,29,.92)!important;border:1px solid rgba(76,145,255,.65)!important;border-radius:9px!important;box-shadow:0 0 18px rgba(58,116,255,.28)!important}

[data-testid="stSidebarCollapsedControl"]{display:flex!important;position:fixed!important;top:.55rem!important;left:.7rem!important;z-index:100000!important}

.block-container{padding:1.25rem 1.6rem 2rem;max-width:1700px}

section[data-testid="stSidebar"]{background:radial-gradient(circle at 50% 12%,rgba(50,117,255,.12),transparent 25%),linear-gradient(180deg,#070a12,#080b14)!important;border-right:1px solid rgba(76,122,255,.18)}

section[data-testid="stSidebar"]>div{padding-top:1.05rem}

.brand-small{text-align:center;font-family:Orbitron,sans-serif;font-size:1.05rem;font-weight:800;letter-spacing:2px;margin-top:-7px}.brand-small span{color:var(--cyan)}.side-caption{text-align:center;color:var(--muted);font-size:.75rem;margin-top:4px}.nav-title{color:#6fdbff;font-size:.70rem;font-weight:800;letter-spacing:1.5px;margin:25px 0 8px}

section[data-testid="stSidebar"] .stButton{width:100%!important;margin:0 0 10px!important}section[data-testid="stSidebar"] .stButton>button{width:100%!important;min-height:58px!important;padding:14px 16px!important;justify-content:flex-start!important;text-align:left!important;border-radius:10px!important;border:1px solid rgba(76,122,255,.24)!important;background:linear-gradient(135deg,rgba(16,22,37,.98),rgba(10,14,25,.98))!important;color:#dce6fa!important;font-size:.92rem!important;font-weight:750!important;box-shadow:none!important}

section[data-testid="stSidebar"] .stButton>button:hover{border-color:rgba(0,210,255,.75)!important;transform:translateX(3px)!important;box-shadow:0 0 20px rgba(33,133,255,.20)!important}

section[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:linear-gradient(90deg,rgba(21,116,255,.98),rgba(112,49,235,.98))!important;color:white!important;border-color:rgba(138,201,255,.8)!important;box-shadow:0 0 22px rgba(71,100,255,.30)!important}

.sidebar-status{margin-top:55px;padding:14px;border:1px solid rgba(83,130,255,.20);border-radius:12px;background:rgba(10,14,25,.8)}.dot{display:inline-block;width:8px;height:8px;background:#20e889;border-radius:50%;box-shadow:0 0 10px #20e889;margin-right:7px}

.top-title{font-size:2.4rem;font-weight:800;margin:0}.top-title span{color:#39a7ff}.top-subtitle{color:#a0aabd;font-size:1.05rem;margin-top:4px}.hero-line{height:1px;background:linear-gradient(90deg,rgba(60,120,255,.55),rgba(130,60,255,.32),transparent);margin:22px 0 26px}

.top-controls{display:flex;align-items:flex-end}.top-controls [data-testid="column"]{display:flex;flex-direction:column;justify-content:flex-end}.top-controls [data-testid="stVerticalBlock"]{gap:0!important}.top-controls .stButton,.top-controls .stDownloadButton{margin:0!important;padding:0!important}.top-controls .stButton>button,.top-controls .stDownloadButton>button{height:42px!important;min-height:42px!important;margin:0!important;align-self:flex-end!important}.top-controls div[data-baseweb="select"],.top-controls div[data-baseweb="select"]>div{min-height:42px!important}.button-align{height:0!important;margin:0!important;padding:0!important;line-height:0!important;font-size:0!important}

.stButton>button,.stDownloadButton>button{border-radius:10px!important;border:1px solid rgba(68,137,255,.55)!important;background:linear-gradient(100deg,#0876df,#5631d6)!important;color:#fff!important;font-weight:700!important;min-height:42px!important;box-shadow:0 0 18px rgba(47,128,255,.16);transition:.2s ease!important}.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:0 0 25px rgba(103,67,255,.35)}

.metric-card{position:relative;overflow:hidden;min-height:118px;padding:18px;border-radius:15px;border:1px solid rgba(87,125,210,.22);background:linear-gradient(145deg,rgba(14,19,32,.97),rgba(7,11,20,.92));box-shadow:0 12px 35px rgba(0,0,0,.24);transition:.25s ease}.metric-card:hover{transform:translateY(-2px);border-color:rgba(70,157,255,.45)}.metric-label{color:#9ca8bc;font-size:.78rem;font-weight:700}.metric-value{font-family:Orbitron,sans-serif;font-size:1.7rem;font-weight:700;margin-top:8px}.metric-foot{color:#718097;font-size:.72rem;margin-top:7px}.icon-blue{color:#4aa8ff}.icon-purple{color:#a871ff}.icon-cyan{color:#4de8ff}

.panel{border:1px solid rgba(88,130,230,.20);background:linear-gradient(145deg,rgba(11,16,28,.97),rgba(6,10,18,.97));border-radius:15px;padding:16px;box-shadow:0 15px 40px rgba(0,0,0,.22)}.panel-title{font-size:1rem;font-weight:800;margin-bottom:4px}.panel-sub{color:#77849a;font-size:.75rem}.section-title{font-size:1.22rem;font-weight:800;margin:5px 0 2px}.section-subtitle{color:#7d8ba2;font-size:.78rem;margin-bottom:12px}.summary-panel{min-height:390px}.summary-row{display:flex;justify-content:space-between;gap:12px;margin:12px 0;color:#8290a7;font-size:.8rem}.summary-row b{color:#f3f6ff}

.stSelectbox label,.stTextInput label{color:#8cdfff!important;font-weight:700!important}div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{background:#0c111e!important;border-color:rgba(76,122,255,.25)!important}div[data-baseweb="select"] span{color:#e8efff!important}

.footer{color:#59677d;font-size:.68rem;text-align:center;padding:20px 0 0}.small-note{color:#6f7e96;font-size:.72rem}

[data-testid="stExpander"]{border:1px solid rgba(83,130,255,.25)!important;border-radius:11px!important;background:rgba(10,15,27,.70)!important;margin-bottom:9px!important}[data-testid="stExpander"] summary{font-weight:750!important;color:#e9f1ff!important}

.amira-table-wrap{width:100%;max-height:520px;overflow:auto;border:1px solid rgba(76,122,255,.25);border-radius:12px;background:#08101c;box-shadow:inset 0 0 25px rgba(22,78,160,.06),0 10px 30px rgba(0,0,0,.18)}.amira-table{width:100%;border-collapse:separate;border-spacing:0;color:#e9f1ff;font-size:.84rem}.amira-table th{position:sticky;top:0;z-index:2;padding:12px 10px;text-align:left;font-weight:800;color:#f4f7ff;background:linear-gradient(135deg,#101b2d,#121a2c);border-bottom:1px solid rgba(76,145,255,.38);white-space:nowrap}.amira-table td{padding:10px;border-bottom:1px solid rgba(76,122,255,.14);background:#0a1422;color:#dbe6f8;white-space:nowrap}.amira-table tbody tr:nth-child(even) td{background:#0c1727}.amira-table tbody tr:hover td{background:#10223a;color:#fff}.amira-table th:first-child{border-top-left-radius:11px}.amira-table th:last-child{border-top-right-radius:11px}.amira-table .num{text-align:right}

.lote-filter-info{margin-top:8px;padding:11px 14px;border:1px solid rgba(32,232,137,.38);border-radius:11px;background:linear-gradient(90deg,rgba(8,61,42,.58),rgba(7,27,30,.70));color:#bfe9d3;font-size:.78rem}.lote-filter-info b{color:#37ef9b}.lote-panel{margin-top:22px}

div[data-testid="stVerticalBlock"] > div:has(.amira-table-wrap){gap:0!important}

</style>""", unsafe_allow_html=True)

def vazio(): return pd.DataFrame(columns=["Data","Hora","Peso (kg)","Lote"])

def formatar_data_planilha(v):

    if pd.isna(v) or str(v).strip()=="": return None

    t=str(v).strip()

    for kwargs in [{"format":"%d/%m/%Y"},{"utc":True},{"dayfirst":True}]:

        try:

            d=pd.to_datetime(t,errors="coerce",**kwargs)

            if not pd.isna(d):

                if getattr(d,"tzinfo",None): d=d.tz_convert(TZ)

                return d.strftime("%d/%m/%Y")

        except: pass

    return t

def formatar_hora_planilha(v):

    if pd.isna(v) or str(v).strip()=="": return None

    t=str(v).strip()

    m=re.match(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$",t)

    if m: return f"{int(m.group(1)):02d}:{m.group(2)}:{m.group(3) or '00'}"

    m=re.match(r"^1899-12-\d{2}T(\d{2}:\d{2}:\d{2})",t)

    if m:return m.group(1)

    try:

        if "T" in t or t.endswith("Z"):

            d=pd.to_datetime(t,utc=True,errors="coerce")

            if not pd.isna(d): return d.tz_convert(TZ).strftime("%H:%M:%S")

    except: pass

    return t

def normalizar_lote(v):

    if pd.isna(v) or not str(v).strip(): return "Sem lote"

    t=re.sub(r"\s+"," ",str(v).strip())

    return t.split(".")[0] if re.fullmatch(r"\d+\.0+",t) else t

def normalizar_colunas(df):

    if df is None or df.empty:return vazio()

    df=df.copy(); ren={}

    for c in df.columns:

        k=str(c).strip().lower().replace(" ","").replace("_","")

        if k in {"peso","peso(kg)","pesokg"}:ren[c]="Peso (kg)"

        elif k=="data":ren[c]="Data"

        elif k=="hora":ren[c]="Hora"

        elif k=="lote":ren[c]="Lote"

    df=df.rename(columns=ren)

    for c in ["Data","Hora","Peso (kg)","Lote"]:

        if c not in df:df[c]=None

    df["Peso (kg)"]=pd.to_numeric(df["Peso (kg)"],errors="coerce")

    df["Data"]=df["Data"].map(formatar_data_planilha);df["Hora"]=df["Hora"].map(formatar_hora_planilha);df["Lote"]=df["Lote"].map(normalizar_lote)

    return df[["Data","Hora","Peso (kg)","Lote"]].dropna(subset=["Peso (kg)"],how="all").reset_index(drop=True)

@st.cache_data(ttl=15)

def carregar_dados_todas_abas():

    r=requests.get(URL_SCRIPT,timeout=20);r.raise_for_status();dados=r.json()

    if not isinstance(dados,dict):raise ValueError("O Google Apps Script não devolveu um JSON de abas.")

    out={}

    for nome,conteudo in dados.items():

        if isinstance(conteudo,list) and conteudo and isinstance(conteudo[0],list):

            out[str(nome)]=normalizar_colunas(pd.DataFrame(conteudo[1:],columns=conteudo[0]))

    return out

def data_da_aba(nome):

    for p,f in [(r"(?<!\d)(\d{2}-\d{2}-\d{4})(?!\d)","%d-%m-%Y"),(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)","%Y-%m-%d")]:

        m=re.search(p,str(nome))

        if m:

            try:return datetime.strptime(m.group(1),f).date()

            except:pass

    return None

def chave_aba(n):

    d=data_da_aba(n);return datetime.combine(d,datetime.min.time()) if d else datetime.min

def rotulo_aba(n):

    d=data_da_aba(n);return d.strftime("%d/%m/%Y") if d else str(n)

def formatar_numero(v):return f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def tabela_amira(df,max_height=520):

    if df is None or df.empty:st.info("Nenhum registro para exibir.");return

    h=f'<div class="amira-table-wrap" style="max-height:{max_height}px"><table class="amira-table"><thead><tr>'

    for c in df.columns:h+=f'<th class="{"num" if c=="Peso (kg)" else ""}">{c}</th>'

    h+="</tr></thead><tbody>"

    for _,r in df.iterrows():

        h+="<tr>"

        for c in df.columns:

            v="" if pd.isna(r[c]) else r[c]

            if c=="Peso (kg)":

                try:v=formatar_numero(float(v))

                except:v=str(v)

            h+=f'<td class="{"num" if c=="Peso (kg)" else ""}">{v}</td>'

        h+="</tr>"

    st.markdown(h+"</tbody></table></div>",unsafe_allow_html=True)

def gerar_xlsx(df):

    b=io.BytesIO()

    try:

        from openpyxl import Workbook

        from openpyxl.styles import Font,PatternFill

        wb=Workbook();ws=wb.active;ws.title="Registros";ws.append(list(df.columns))

        for c in ws[1]:c.font=Font(bold=True,color="FFFFFF");c.fill=PatternFill("solid",fgColor="111827")

        for r in df.itertuples(index=False,name=None):ws.append(list(r))

        ws.freeze_panes="A2";ws.auto_filter.ref=ws.dimensions

        for col in ws.columns:

            letra=col[0].column_letter;maior=max(len(str(c.value or "")) for c in col);ws.column_dimensions[letra].width=min(max(maior+2,12),28)

        wb.save(b);return b.getvalue()

    except:return df.to_csv(index=False,sep=";").encode("utf-8-sig")

def grafico_layout(fig,height=300):

    fig.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#aeb9cb",family="Inter"),margin=dict(l=10,r=10,t=20,b=10),height=height,showlegend=False,xaxis=dict(gridcolor="rgba(90,120,180,.10)",zeroline=False),yaxis=dict(gridcolor="rgba(90,120,180,.10)",zeroline=False))

    return fig

def mostrar_metricas(df):

    peso=float(df["Peso (kg)"].sum()) if not df.empty else 0;media=float(df["Peso (kg)"].mean()) if not df.empty else 0

    cards=[("📦","Caixas Passadas",str(len(df)),"Registros filtrados","cyan"),("⚖","Peso Total (kg)",formatar_numero(peso),"Peso acumulado","blue"),("◈","Média por Caixa",f"{formatar_numero(media)} kg","Média dos registros","purple")]

    for col,(i,l,v,f,c) in zip(st.columns(3),cards):

        with col:st.markdown(f'<div class="metric-card"><div class="metric-label"><span class="icon-{c}">{i}</span>&nbsp;&nbsp;{l}</div><div class="metric-value">{v}</div><div class="metric-foot">{f}</div></div>',unsafe_allow_html=True)

def agrupar_por_lote(df):

    if df is None or df.empty:return pd.DataFrame(columns=["Lote","Pesagens","Peso total (kg)","Média (kg)"])

    x=df.copy();x["Lote"]=x["Lote"].map(normalizar_lote)

    g=x.groupby("Lote",dropna=False).agg(Pesagens=("Peso (kg)","count"),**{"Peso total (kg)":("Peso (kg)","sum"),"Média (kg)":("Peso (kg)","mean")}).reset_index()

    g["_o"]=g.Lote.map(lambda v:(0,int(v)) if str(v).isdigit() else (1,str(v).lower()))

    return g.sort_values("_o").drop(columns="_o").reset_index(drop=True)

def mostrar_producao_por_lote(df):

    g=agrupar_por_lote(df)

    st.markdown('<div class="panel lote-panel"><div class="panel-title" style="font-size:1.15rem;">📦 Produção por Lote</div><div class="panel-sub" style="font-size:.80rem;margin-bottom:14px;">O sistema agrupa automaticamente todas as pesagens que possuem o mesmo lote.</div>',unsafe_allow_html=True)

    if g.empty:st.info("Não há lotes para agrupar.");st.markdown("</div>",unsafe_allow_html=True);return

    ex=g.copy()

    for c in ["Peso total (kg)","Média (kg)"]:ex[c]=ex[c].round(2).map(formatar_numero)

    tabela_amira(ex,max_height=360)

    c1,c2=st.columns(2)

    with c1:

        st.markdown('<div class="panel-title">⚖ Peso total por lote</div>',unsafe_allow_html=True)

        f=px.bar(g,x="Lote",y="Peso total (kg)",text="Peso total (kg)");f.update_traces(marker_color="#2f80ff",texttemplate="%{text:.2f}",textposition="outside",cliponaxis=False);f.update_layout(yaxis_title="Peso (kg)",xaxis_title="Lote");st.plotly_chart(grafico_layout(f,280),use_container_width=True,config={"displayModeBar":False})

    with c2:

        st.markdown('<div class="panel-title">📦 Pesagens por lote</div>',unsafe_allow_html=True)

        f=px.bar(g,x="Lote",y="Pesagens",text="Pesagens");f.update_traces(marker_color="#8a35ff",texttemplate="%{text}",textposition="outside",cliponaxis=False);f.update_layout(yaxis_title="Quantidade",xaxis_title="Lote");st.plotly_chart(grafico_layout(f,280),use_container_width=True,config={"displayModeBar":False})

    st.markdown("</div>",unsafe_allow_html=True)

try:dados_abas=carregar_dados_todas_abas();erro_api=None

except Exception as e:dados_abas={};erro_api=str(e)

lista_abas=sorted(dados_abas,key=chave_aba,reverse=True)

dia_atual=st.session_state.get("dia_selecionado",lista_abas[0] if lista_abas else None)

if dia_atual not in lista_abas and lista_abas:dia_atual=lista_abas[0]

lote_atual=st.session_state.get("lote_selecionado","Todos os lotes")

with st.sidebar:

    if os.path.exists("logo.png"):st.image("logo.png",use_container_width=True)

    elif os.path.exists("logo.jpg"):st.image("logo.jpg",use_container_width=True)

    st.markdown('<div class="brand-small">Sistema <span>AMIRA</span></div><div class="side-caption">Monitoramento • Automação • Precisão</div><div class="nav-title">MENU DE NAVEGAÇÃO</div>',unsafe_allow_html=True)

    opcoes=["📋  Registro e Dados","📊  Gráficos e Análises","🗂  Histórico de Planilhas"];menu=st.session_state.get("menu_amira",opcoes[0])

    for i,o in enumerate(opcoes):

        if st.button(o,key=f"menu_amira_{i}",type="primary" if menu==o else "secondary",use_container_width=True):st.session_state["menu_amira"]=o;st.rerun()

    st.markdown('<div class="sidebar-status"><b>Sistema AMIRA</b><div style="color:#7f8da4;font-size:.75rem;margin-top:5px;"><span class="dot"></span>Monitoramento ativo</div></div><div class="footer">©️ 2026 AMIRA • SENAI<br>IoT • Automação • Precisão</div>',unsafe_allow_html=True)

titulos={"📋  Registro e Dados":("<span>Bem-vindo à</span> AMIRA","Sistema de Monitoramento e Registro de Produção"),"📊  Gráficos e Análises":("<span>Gráficos</span> e Análises","Explore o histórico e compare dias e meses de produção."),"🗂  Histórico de Planilhas":("<span>Histórico</span> de Planilhas","Controle de lançamentos no sistema da empresa.")}

t,s=titulos[menu];st.markdown(f'<div class="top-title">{t}</div><div class="top-subtitle">{s}</div><div style="margin-top:15px"></div>',unsafe_allow_html=True)

st.markdown('<div class="top-controls">',unsafe_allow_html=True)

col_dia,col_lote,col_b1,col_b2=st.columns([1.25,1.25,.9,.9],gap="small")

with col_dia:

    if menu=="📋  Registro e Dados" and lista_abas:

        novo=st.selectbox("📅 Dia de Produção",lista_abas,format_func=rotulo_aba,index=lista_abas.index(dia_atual) if dia_atual in lista_abas else 0,key="select_dia_amira")

        if novo!=dia_atual:st.session_state["dia_selecionado"]=novo;st.session_state["lote_selecionado"]="Todos os lotes";st.rerun()

        dia_atual=novo

df=dados_abas.get(dia_atual,vazio()) if dia_atual else vazio()

with col_lote:

    if menu=="📋  Registro e Dados" and not df.empty:

        lotes=sorted(df["Lote"].map(normalizar_lote).drop_duplicates().tolist(),key=lambda x:(0,int(x)) if str(x).isdigit() else (1,str(x).lower()))

        op=["Todos os lotes"]+lotes

        if lote_atual not in op:lote_atual="Todos os lotes"

        novo=st.selectbox("🔎 Filtrar por lote",op,index=op.index(lote_atual),key="select_lote_amira")

        if novo!=lote_atual:st.session_state["lote_selecionado"]=novo;st.rerun()

        lote_atual=novo

df_filtrado=df[df["Lote"].map(normalizar_lote)==lote_atual].copy() if menu=="📋  Registro e Dados" and lote_atual!="Todos os lotes" else df.copy()

with col_b1:

    if menu=="📋  Registro e Dados":

        if st.button("🔄 Recarregar Dados",use_container_width=True,key="recarregar_amira"):carregar_dados_todas_abas.clear();st.rerun()

with col_b2:

    if menu=="📋  Registro e Dados" and dia_atual and not df_filtrado.empty:

        st.download_button("⬇️ Baixar Planilha",data=gerar_xlsx(df_filtrado),file_name=f"AMIRA_Producao_{rotulo_aba(dia_atual).replace('/','-')}{('_Lote_'+str(lote_atual)) if lote_atual!='Todos os lotes' else ''}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True,key="download_amira")

st.markdown('</div><div class="hero-line"></div>',unsafe_allow_html=True)

if menu=="📋  Registro e Dados":

    if lote_atual!="Todos os lotes" and not df_filtrado.empty:st.markdown(f'<div class="lote-filter-info">🔎 Filtro ativo: <b>Lote {lote_atual}</b> • Exibindo apenas as pesagens desse lote.</div>',unsafe_allow_html=True)

    elif not df.empty:st.markdown('<div class="lote-filter-info">🟢 <b>Todos os lotes</b> • O sistema agrupou automaticamente os registros iguais.</div>',unsafe_allow_html=True)

    st.markdown('<div class="section-title">Dados do Dia</div>',unsafe_allow_html=True);mostrar_metricas(df_filtrado);st.markdown("<br>",unsafe_allow_html=True);mostrar_producao_por_lote(df_filtrado);st.markdown("<br><div class='section-title' style='font-size:1.2rem;'>📋 Registros de Produção</div><div class='section-subtitle'>Pesagens registradas no dia selecionado.</div>",unsafe_allow_html=True)

    if df_filtrado.empty:st.info("Aguardando pesagens para exibir na tabela.")

    else:

        ex=df_filtrado.copy().reset_index(drop=True);ex.insert(0,"#",ex.index+1);tabela_amira(ex,440)

    st.markdown("<br>",unsafe_allow_html=True)

    peso=float(df_filtrado["Peso (kg)"].sum()) if not df_filtrado.empty else 0;media=float(df_filtrado["Peso (kg)"].mean()) if not df_filtrado.empty else 0

    st.markdown(f'<div class="panel summary-panel"><div class="panel-title">Resumo do Dia</div><div class="panel-sub">Indicadores principais</div><div style="display:flex;justify-content:center;align-items:center;padding:30px 0 25px;"><div style="width:145px;height:145px;border-radius:50%;background:conic-gradient(#3d8cff 85%,rgba(255,255,255,.05) 85%);display:flex;justify-content:center;align-items:center;"><div style="width:125px;height:125px;border-radius:50%;background:#080c14;display:flex;flex-direction:column;justify-content:center;align-items:center;"><span style="font-family:Orbitron;font-size:1.35rem;font-weight:800;color:#fff">{formatar_numero(peso)}</span><span style="font-size:.75rem;color:#77849a">kg</span></div></div></div><div class="summary-row"><span>📦 Caixas passadas</span><b>{len(df_filtrado)}</b></div><div class="summary-row"><span>↗️ Média por caixa</span><b>{formatar_numero(media)} kg</b></div><div class="summary-row"><span>⚖ Peso total acumulado</span><b>{formatar_numero(peso)} kg</b></div></div>',unsafe_allow_html=True)

    st.markdown("<br><br><div class='section-title' style='font-size:1.2rem;'>Desempenho do Dia</div>",unsafe_allow_html=True)

    g1,g2=st.columns(2)

    with g1:

        st.markdown('<div class="panel-title">Peso ao longo do dia</div>',unsafe_allow_html=True)

        if not df_filtrado.empty:

            x=df_filtrado.reset_index(drop=True).copy();x["Registro"]=x.index+1;f=px.area(x,x="Registro",y="Peso (kg)");f.update_traces(line_color="#3d8cff",fillcolor="rgba(61,140,255,.15)");st.plotly_chart(grafico_layout(f),use_container_width=True,config={"displayModeBar":False})

    with g2:

        st.markdown('<div class="panel-title">Distribuição dos pesos</div>',unsafe_allow_html=True)

        if not df_filtrado.empty:

            f=px.histogram(df_filtrado,x="Peso (kg)",nbins=8);f.update_traces(marker_color="#7d4cff",marker_line_color="#05070d",marker_line_width=2);f.update_layout(bargap=.08);st.plotly_chart(grafico_layout(f),use_container_width=True,config={"displayModeBar":False})

elif menu=="📊  Gráficos e Análises":

    if not lista_abas:st.info("Aguardando registros para gerar as análises.")

    else:

        st.markdown('<div class="panel-title" style="font-size:1.15rem;color:#00d2ff;">Comparativo Diário</div><div class="section-subtitle">Produção dia a dia</div>',unsafe_allow_html=True)

        resumo=[{"Data":rotulo_aba(n),"Peso total (kg)":t["Peso (kg)"].sum(),"Caixas":len(t)} for n,t in dados_abas.items() if not t.empty];rdf=pd.DataFrame(resumo)

        if not rdf.empty:

            c1,c2=st.columns(2)

            with c1:

                st.markdown('<div class="panel-title">Peso Diário (kg)</div>',unsafe_allow_html=True);f=px.bar(rdf,x="Data",y="Peso total (kg)");f.update_traces(marker_color="#2f80ff");st.plotly_chart(grafico_layout(f),use_container_width=True,config={"displayModeBar":False})

            with c2:

                st.markdown('<div class="panel-title">Caixas por Dia</div>',unsafe_allow_html=True);f=px.bar(rdf,x="Data",y="Caixas");f.update_traces(marker_color="#8a35ff");st.plotly_chart(grafico_layout(f),use_container_width=True,config={"displayModeBar":False})

        st.markdown('<br><div class="panel-title" style="font-size:1.15rem;color:#00d2ff;">Análise de Longo Prazo (Mensal)</div><div class="section-subtitle">Comparativo histórico agrupado por mês e ano para controle gerencial.</div>',unsafe_allow_html=True)

        lt=[]

        for n,t in dados_abas.items():

            if not t.empty and data_da_aba(n):

                d=data_da_aba(n);lt.append({"Ano":str(d.year),"Mês_Num":d.month,"Mês/Ano":f"{d.month:02d}/{d.year}","Peso total (kg)":t["Peso (kg)"].sum(),"Caixas":len(t)})

        if lt:

            x=pd.DataFrame(lt).groupby(["Ano","Mês_Num","Mês/Ano"]).sum().reset_index().sort_values(["Ano","Mês_Num"]);a,b=st.columns(2)

            with a:

                st.markdown('<div class="panel-title">Produção Mensal Acumulada (kg)</div>',unsafe_allow_html=True);f=px.bar(x,x="Mês/Ano",y="Peso total (kg)",color="Ano",color_discrete_sequence=["#00d2ff","#2f80ff","#8a35ff"]);st.plotly_chart(grafico_layout(f),use_container_width=True,config={"displayModeBar":False})

            with b:

                st.markdown('<div class="panel-title">Volume Mensal (Qtd. Caixas)</div>',unsafe_allow_html=True);f=px.line(x,x="Mês/Ano",y="Caixas",color="Ano",markers=True,color_discrete_sequence=["#00d2ff","#2f80ff","#8a35ff"]);f.update_traces(line_width=3,marker=dict(size=8));st.plotly_chart(grafico_layout(f),use_container_width=True,config={"displayModeBar":False})

        else:st.info("Aguardando dados históricos suficientes para gerar gráficos mensais.")

else:

    st.markdown('<div class="section-title">Histórico de Planilhas</div>',unsafe_allow_html=True)

    if not lista_abas:st.info("Ainda não há planilhas registradas pela balança.")

    else:

        for n in lista_abas:

            t=dados_abas.get(n,vazio());r=rotulo_aba(n)

            with st.expander(f"📅 {r}",expanded=False):

                if t.empty:st.info("A planilha existe, mas ainda não possui registros.")

                else:

                    ex=t.copy().reset_index(drop=True);ex.insert(0,"#",ex.index+1);tabela_amira(ex,430);g=agrupar_por_lote(t)

                    if not g.empty:

                        for c in ["Peso total (kg)","Média (kg)"]:g[c]=g[c].map(formatar_numero)

                        st.markdown('<div class="panel-title" style="margin-top:18px;">📦 Resumo por lote</div>',unsafe_allow_html=True);tabela_amira(g,300)

st.markdown('<div class="footer">AMIRA • Sistema de Monitoramento e Registro de Produção • SENAI</div>',unsafe_allow_html=True)

'''

print(path)
