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

if __name__ == "__main__":
    
    if not os.path.exists('./src/static'):
            os.makedirs('./src/static')
        
    # Injeção de Dependência para o Robô
    repo = GerenciadorCandidatosService('./src/static/candidatos.json')
    saidas = [GeradorPDFService(), GeradorRSSService()]
    
    # Dependência de Publicação
    publicador = None
    # try:
    #     token = obter_config("LINKEDIN_PAGE_ACCESS_TOKEN")
    #     org_id = obter_config("LINKEDIN_ORG_ID")
        
    #     if token and org_id:
    #         publicador = LinkedInPublisherService(token, org_id)
    # except Exception:
    #     print("Aviso: Secrets do LinkedIn não encontrados.")
        
    # Orquestração
    app = JornalDiarioService(repo, saidas, publicador)
    app.processar_edicao_do_dia()