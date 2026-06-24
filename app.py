import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página da Web
st.set_page_config(page_title="Controle de Pesagem - Mussarela", page_icon="🧀", layout="centered")

st.title("🧀 Controle de Produção e Pesagem")
st.subheader("Registros Sincronizados com o Google Sheets")

# ⚠️ SUBSTITUA O LINK ABAIXO PELO LINK DE COMPARTILHAMENTO DA SUA PLANILHA!
# Você deve ir na sua planilha do Google, clicar em "Compartilhar", colocar como "Qualquer pessoa com o link pode ler", copiar o link e colar aqui.
LINK_DA_PLANILHA = "https://docs.google.com/spreadsheets/d/1lx5pbPRlsT9BH4Z9N3cI1apf7UBc1u3q79TeNN_T-uA/edit?usp=sharing"

# Função para converter o link normal da planilha em um link de download de dados
def converter_link_csv(link):
    try:
        id_planilha = link.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv"
    except:
        return None

url_csv = converter_link_csv(LINK_DA_PLANILHA)

# Botão de Atualização
if st.button("🔄 Atualizar Dados da Balança"):
    st.rerun()

st.markdown("---")

st.markdown("### 📋 Registros Recentes (Direto do Banco de Dados)")

if url_csv:
    try:
        # Lê os dados da planilha do Google em tempo real
        df = pd.read_csv(url_csv)
        
        if not df.empty:
            st.dataframe(df.tail(20), use_container_width=True) # Mostra os últimos 20 registros
            
            # Botão de download do Excel
            csv_dados = df.to_csv(index=False, sep=";").encode('utf-8-sig')
            st.download_button(
                label="📥 Baixar Planilha para o Excel",
                data=csv_dados,
                file_name=f"pesagem_mussarela_{datetime.now().strftime('%Y-%m-%d')}.csv",
                mime="text/csv",
            )
        else:
            st.info("A planilha do Google está vazia. Aguardando dados do Arduino...")
    except Exception as e:
        st.error("Erro ao conectar com a Planilha do Google. Verifique se o link está correto e público.")
else:
    st.warning("Por favor, configure o link da sua planilha do Google no código.")
