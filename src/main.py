from infrastructure.repositories.candidato_repository import CandidatoRepository
from infrastructure.external_api.linkedin.linkedin_service import LinkedInService
from application.services.registrar_candidato_service import RegistrarCandidatoService
from ui.app_view import renderizar_interface
import streamlit as st

# 1. Montagem da Máquina (Injeção)
repo = CandidatoRepository()
auth = LinkedInService(
    client_id=st.secrets["LINKEDIN_CLIENT_ID"],
    client_secret=st.secrets["LINKEDIN_CLIENT_SECRET"],
    redirect_uri=st.secrets["REDIRECT_URI"]
)
service = RegistrarCandidatoService(repo, auth)

# 2. Chamada da UI
renderizar_interface(service, auth)