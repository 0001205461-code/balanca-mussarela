import pandas as pd
import streamlit as st

# Configuração da página da Web
st.set_page_config(
    page_title="Controle de Pesagem - Mussarela",
    page_icon="🧀",
    layout="centered",
)

st.title("🧀 Controle de Produção e Pesagem")
st.subheader("Registros Sincronizados com o Google Sheets")

# ⚠️ SUBSTUA PELO SEU LINK DE COMPARTILHAMENTO DA PLANILHA DO GOOGLE ⚠️
LINK_DA_PLANILHA = (
    "https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit?usp=sharing"
)


def converter_links_planilha(link):
  try:
    id_planilha = link.split("/d/")[1].split("/")[0]
    # Link interno para o Streamlit ler os dados na tela
    url_csv = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv"
    # Link direto para baixar o arquivo no formato Excel (.xlsx)
    url_xlsx = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=xlsx"
    return url_csv, url_xlsx
  except:
    return None, None


url_csv, url_xlsx = converter_links_planilha(LINK_DA_PLANILHA)

# Botão de Atualização da tela
if st.button("🔄 Atualizar Dados da Balança"):
  st.rerun()

st.markdown("---")

# Botão direto para abrir no Google Planilhas
st.link_button("🌐 Abrir Planilha no Google Sheets (Navegador)", LINK_DA_PLANILHA)

st.markdown("### 📋 Registros Recentes (Direto do Banco de Dados)")

if url_csv and url_xlsx:
  try:
    # Leitura dos dados atualizados
    df = pd.read_csv(url_csv)

    if not df.empty:
      # Exibe as últimas 20 pesagens na tabela do site
      st.dataframe(df.tail(20), use_container_width=True)

      st.markdown("---")

      # Botão que baixa o arquivo oficial .xlsx
      st.link_button("📥 Baixar Planilha em Excel (.xlsx)", url_xlsx)
    else:
      st.info(
          "A planilha do Google está vazia. Aguardando dados do Arduino..."
      )
  except Exception as e:
    st.error(
        "Erro ao conectar com a Planilha do Google. Verifique se o link está"
        " correto e público."
    )
else:
  st.warning(
      "Por favor, configure o link da sua planilha do Google no código."
  )
