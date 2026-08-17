import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Controle de Produção e Pesagem",
    page_icon="🧀",
    layout="centered"
)

# Insira aqui a URL de exportação CSV da sua Planilha do Google ou da sua Web App
# Para pegar a URL CSV do Google Sheets: Vá em Arquivo > Compartilhar > Publicar na Web > Escolha CSV
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA/export?format=csv"


# ---------------------------------------------------------
# FUNÇÃO PARA CARREGAR OS DADOS
# ---------------------------------------------------------
@st.cache_data(ttl=5)
def carregar_dados():
    try:
        # Lê os dados da planilha diretamente para um DataFrame
        df = pd.read_csv(URL_PLANILHA)
        return df
    except Exception as e:
        # Retorna DataFrame vazio em caso de falha de conexão
        return pd.DataFrame()


# ---------------------------------------------------------
# INTERFACE DO STREAMLIT
# ---------------------------------------------------------
st.title("🧀 Controle de Produção e Pesagem")
st.write("### Registros Sincronizados com o Google Sheets")

# Botão que limpa o cache e força a atualização imediata dos dados
if st.button("🔄 Atualizar Dados da Balança"):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

st.write("### 📋 Registros Recentes (Direto do Banco de Dados)")

# Carrega os dados da planilha
df = carregar_dados()

if not df.empty:
    # Exibe a tabela na tela
    st.dataframe(df, use_container_width=True)

    # Converte o DataFrame para CSV compatível com Excel (utf-8-sig)
    csv = df.to_csv(index=False).encode('utf-8-sig')

    # Botão para baixar o arquivo em Excel/CSV
    st.download_button(
        label="📥 Baixar Planilha para o Excel",
        data=csv,
        file_name="Controle_de_Pesagem_Mussarela.csv",
        mime="text/csv",
    )
else:
    st.warning("Ainda não há dados carregados ou a URL da planilha precisa ser verificada.")
