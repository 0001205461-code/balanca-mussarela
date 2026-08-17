# AMIRA — Balança Mussarela

Painel Streamlit do protótipo AMIRA para monitoramento de pesagens.

## Fluxo
ESP32 → Google Apps Script → Google Sheets → painel AMIRA.

O Apps Script cria automaticamente uma aba com o nome `dd-MM-yyyy` no primeiro registro de cada dia e grava:

`Data | Hora | Peso (kg) | Lote`

## Publicação
1. Atualize o `google_apps_script.gs` na planilha.
2. Publique o Apps Script como Aplicativo da Web.
3. Confirme que a URL publicada é a mesma de `URL_SCRIPT` em `app.py`.
4. No GitHub/Streamlit Cloud, mantenha `app.py`, `logo.jpg` e `requirements.txt` na mesma pasta.
5. Faça um novo deploy/reboot para instalar as dependências.

## Download
O botão Baixar Planilha gera XLSX com `openpyxl`. Se o ambiente estiver temporariamente sem a biblioteca, o código possui fallback seguro para CSV e não derruba o dashboard.
