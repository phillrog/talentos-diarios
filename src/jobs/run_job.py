from application.services.gerenciador_candidatos_service import GerenciadorCandidatosService
from application.services.jornal_diario_service import JornalDiarioService
from infrastructure.services.gerador_pdf_service import GeradorPDFService
from infrastructure.services.gerador_rss_service import GeradorRSSService
from infrastructure.external_api.linkedin.linkedin_publisher_service import LinkedInPublisherService
import os
from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()

def obter_config(chave):
    try:
        # Tenta pegar do Streamlit (se estiver rodando via streamlit run)
        return st.secrets[chave]
    except:
        # Se falhar, pega das variáveis de ambiente (arquivo .env ou GitHub Secrets)
        return os.getenv(chave)
    
def obter_id():
    access_token = obter_config("LINKEDIN_PAGE_ACCESS_TOKEN")
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get("sub") # ESSE É O CARA!
        print(f"Seu ID real para o secrets: {user_id}")
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        
def disparar_onesignal():

    app_id = os.getenv("ONESIGNAL_APP_ID")
    api_key = os.getenv("ONESIGNAL_REST_API_KEY")
    template_id = os.getenv("ONESIGNAL_TEMPLATE_ID")

    if not app_id or not api_key:
        print("⚠️ OneSignal ignorado: Chaves não encontradas.")
        return

    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "app_id": app_id,
        "template_id": template_id,
        "included_segments": ["All"]
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"📡 OneSignal: {response.status_code} - {response.text}")        

if __name__ == "__main__":
    
    if not os.path.exists('./src/static'):
            os.makedirs('./src/static')
        
    # Injeção de Dependência para o Robô
    repo = GerenciadorCandidatosService('./src/static/candidatos.json')
    saidas = [GeradorPDFService(), GeradorRSSService()]
    
    # Dependência de Publicação
    publicador = None
        
    # Orquestração
    app = JornalDiarioService(repo, saidas, publicador)
    app.processar_edicao_do_dia()
    
    disparar_onesignal()