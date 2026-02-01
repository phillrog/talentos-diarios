from application.services.gerenciador_candidatos_service import GerenciadorCandidatosService
from application.services.jornal_diario_service import JornalDiarioService
from infrastructure.services.gerador_pdf_service import GeradorPDFService
from infrastructure.services.gerador_rss_service import GeradorRSSService
from infrastructure.external_api.linkedin.linkedin_publisher_service import LinkedInPublisherService
import os
from dotenv import load_dotenv
import streamlit as st
import requests
import onesignal
from onesignal.api import default_api
from onesignal.model.generic_error import GenericError
from onesignal.model.notification import Notification
from onesignal.model.create_notification_success_response import CreateNotificationSuccessResponse
from pprint import pprint

load_dotenv()

def obter_config(chave):
    try:
        # Tenta pegar do Streamlit (se estiver rodando via streamlit run)
        return st.secrets[chave]
    except:
        # Se falhar, pega das variáveis de ambiente (arquivo .env ou GitHub Secrets)
        return os.getenv(chave)
    
def disparar_onesignal():
    app_id = obter_config("ONESIGNAL_APP_ID")
    api_key = obter_config("ONESIGNAL_REST_API_KEY")
    template_id = obter_config("ONESIGNAL_TEMPLATE_ID")

    if not app_id or not api_key:
        print("⚠️ OneSignal ignorado: Chaves não encontradas.")
        return

    # --- 1. CONFIGURAÇÃO (Aqui estava o erro: era Configuration, não Notification) ---
    configuration = onesignal.Configuration(
        app_key = api_key
    )

    # --- 2. CLIENTE API ---
    with onesignal.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        
        # --- 3. MONTAGEM DA NOTIFICAÇÃO ---
        notification = Notification(
            app_id = app_id,
            template_id = template_id,
            included_segments = ["Total Subscriptions"] 
        )

        try:
            # --- 4. ENVIO ---
            api_response = api_instance.create_notification(notification)
            print("📡 Resposta do OneSignal:")
            pprint(api_response)
        except onesignal.ApiException as e:
            print(f"❌ Erro ao chamar OneSignal: {e}")
            # Se der erro de 'id', é porque não há inscritos

            
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