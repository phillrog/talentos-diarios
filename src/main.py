from infrastructure.repositories.candidato_repository import CandidatoRepository
from infrastructure.external_api.linkedin.linkedin_service import LinkedInService
from application.services.registrar_candidato_service import RegistrarCandidatoService
from ui.app_view import renderizar_interface
import streamlit as st
import streamlit.components.v1 as components

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

if "onesignal_injetado" not in st.session_state:
    components.html(
        """
        <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
        <script>
          window.OneSignalDeferred = window.OneSignalDeferred || [];
          window.OneSignalDeferred.push(async function(OneSignal) {
            await OneSignal.init({
              appId: "66267c67-6b67-4742-a72d-25c884d2fe17",
            });
          });
        </script>
        """,
        height=0,
    )
    st.session_state["onesignal_injetado"] = True