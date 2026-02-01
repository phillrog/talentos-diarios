from application.services.gerenciador_candidatos_service import GerenciadorCandidatosService
from application.services.jornal_diario_service import JornalDiarioService
from infrastructure.services.gerador_pdf_service import GeradorPDFService
from infrastructure.services.gerador_rss_service import GeradorRSSService

import os
from dotenv import load_dotenv
import streamlit as st
import requests


load_dotenv()

def obter_config(chave):
    # Tenta Streamlit
    try:
        if chave in st.secrets:
            return st.secrets[chave]
    except:
        pass
    
    # Tenta Variável de Ambiente
    valor = os.getenv(chave)
    if valor:
        return valor
    
    print(f"❌ ALERTA: A chave {chave} não foi encontrada em lugar nenhum!")
    return None
 
##def disparar_notificacao(titulo, mensagem):
    
            
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
    
    