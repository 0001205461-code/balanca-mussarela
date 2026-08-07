import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuração da página da Web
st.set_page_config(page_title="Controle de Pesagem - Mussarela", page_icon="🧀", layout="centered")

st.title("🧀 Controle de Produção e Pesagem")
st.subheader("Registros Sincronizados com o Google Sheets")

# Cole aqui o LINK DE COMPARTILHAMENTO da sua planilha do Google
LINK_DA_PLANILHA = "https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit?usp=sharing"

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

# Botão direto para abrir no Google Planilhas na web
st.link_button("🌐 Abrir Planilha no Google Sheets (Navegador)", LINK_DA_PLANILHA)

st.markdown("### 📋 Registros Recentes (Direto do Banco de Dados)")

if url_csv:
    try:
        df = pd.read_csv(url_csv)
        
        if not df.empty:
            st.dataframe(df.tail(20), use_container_width=True)
            
            # Gerar arquivo em formato Excel (.xlsx) real
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Pesagens')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Baixar Planilha em Excel (.xlsx)",
                data=excel_data,
                file_name=f"pesagem_mussarela_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.info("A planilha do Google está vazia. Aguardando dados do Arduino...")
    except Exception as e:
        st.error("Erro ao conectar com a Planilha do Google. Verifique o link e se está público.")
else:
    st.warning("Por favor, configure o link da sua planilha do Google no código.")
