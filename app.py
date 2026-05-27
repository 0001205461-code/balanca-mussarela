import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página da Web
st.set_page_config(page_title="Controle de Pesagem - Mussarela", page_icon="🧀", layout="centered")

NOME_ARQUIVO = "registro_pesagem.csv"

# Função para carregar os dados existentes
def carregar_dados():
    if os.path.exists(NOME_ARQUIVO):
        return pd.read_csv(NOME_ARQUIVO, sep=";")
    else:
        return pd.DataFrame(columns=['Data', 'Hora', 'Peso (kg)', 'Lote'])

# Inicializa o banco de dados na sessão do site
if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()

# --- INTERFACE DO NAVEGADOR (O que o funcionário vai ver) ---
st.title("🧀 Controle de Produção e Pesagem")
st.subheader("Registros Recebidos da Balança Industrial")

# Botões de Atualização e Download
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Atualizar Dados"):
        st.session_state.dados = carregar_dados()
        st.rerun()

with col2:
    # Transforma os dados em Excel para download
    df_atual = st.session_state.dados
    csv = df_atual.to_csv(index=False, sep=";").encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar Planilha para o Excel",
        data=csv,
        file_name=f"pesagem_mussarela_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
    )

st.markdown("---")

# Exibe a tabela na tela do navegador
st.markdown("### 📋 Registros Recentes")
if not st.session_state.dados.empty:
    st.dataframe(st.session_state.dados.tail(20), use_container_width=True) # Mostra os últimos 20 registros
else:
    st.info("Nenhum registro encontrado ainda. Aguardando dados da balança...")

# --- ROTA DE RECEPÇÃO PARA O ARDUINO (Invisível no navegador) ---
# O Arduino vai acessar esse link enviando os parâmetros na URL
query_params = st.query_params

if "peso" in query_params and "lote" in query_params:
    peso = query_params["peso"]
    lote = query_params["lote"]
    
    # Captura data e hora atuais
    agora = datetime.now()
    data_atual = agora.strftime('%d/%m/%Y')
    hora_atual = agora.strftime('%H:%M:%S')
    
    # Salva no arquivo
    nova_linha = pd.DataFrame([[data_atual, hora_atual, peso, lote]], columns=['Data', 'Hora', 'Peso (kg)', 'Lote'])
    nova_linha.to_csv(NOME_ARQUIVO, mode='a', header=not os.path.exists(NOME_ARQUIVO), index=False, sep=";")
    
    # Limpa os parâmetros da URL para não repetir o registro no próximo carregamento
    st.query_params.clear()
    
    # Mostra um aviso rápido na tela e responde OK para a rede
    st.success(f"Novo peso registrado: {peso}kg | Lote: {lote}")
    st.write("OK") # Resposta que o Arduino lê para acender o LED Verde
