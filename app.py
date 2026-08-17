import streamlit as st
import pandas as pd
import requests

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Controle de Produção e Pesagem",
    page_icon="🧀",
    layout="centered"
)

# Sua URL do Google Apps Script
URL_SCRIPT = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQMSV65oJIbDvYnkxlgJGUlNyvxfXwQ5sBG_28QbZ_QjtnPNIipLvS1MSwfbmZThhu1TT1hEcFDmiIs/pub?output=csv"


# ---------------------------------------------------------
# FUNÇÃO PARA CARREGAR OS DADOS (SEM CACHE PRESO)
# ---------------------------------------------------------
@st.cache_data(ttl=2)
def carregar_dados():
    try:
        # Faz a requisição HTTP para o seu Apps Script
        resposta = requests.get(URL_SCRIPT)
        
        # Tenta interpretar como JSON/Lista de Dados
        dados = resposta.json()
        
        # Converte para DataFrame do Pandas (A primeira linha vira o cabeçalho)
        df = pd.DataFrame(dados[1:], columns=dados[0])
        return df
    except Exception as e:
        # Se o script não retornar JSON, tenta ler via CSV direto
        try:
            df = pd.read_csv(URL_SCRIPT)
            return df
        except:
            return pd.DataFrame()


# ---------------------------------------------------------
# INTERFACE DO STREAMLIT
# ---------------------------------------------------------
st.title("🧀 Controle de Produção e Pesagem")
st.write("### Registros Sincronizados com o Google Sheets")

# Botão de Atualizar que LIMPA O CACHE e força o recarregamento
if st.button("🔄 Atualizar Dados da Balança"):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

st.write("### 📋 Registros Recentes (Direto do Banco de Dados)")

# Carrega os dados atualizados
df = carregar_dados()

if not df.empty:
    # Exibe a tabela na tela
    st.dataframe(df, use_container_width=True)

    # Converte para CSV para download no Excel
    csv = df.to_csv(index=False).encode('utf-8-sig')

    # Botão para Baixar Planilha
    st.download_button(
        label="📥 Baixar Planilha para o Excel",
        data=csv,
        file_name="Controle_de_Pesagem_Mussarela.csv",
        mime="text/csv",
    )
else:
    st.warning("Carregando ou aguardando novos registros da balança...")
