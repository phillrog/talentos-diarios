import sys
import os
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# --- 1. SETUP DE PATHS (Obrigatório no topo) ---
file_path = Path(__file__).resolve()
src_path = file_path.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

# --- 2. INJEÇÃO ÚNICA DO ONESIGNAL ---
if "onesignal_injetado" not in st.session_state:
    components.html(
        """
        <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
        <script>
          window.OneSignalDeferred = window.OneSignalDeferred || [];
          window.OneSignalDeferred.push(async function(OneSignal) {
            console.log("OneSignal: Inicializando pela primeira vez...");
            await OneSignal.init({
              appId: "66267c67-6b67-4742-a72d-25c884d2fe17",
            });
          });
        </script>
        """,
        height=0,
    )
    st.session_state["onesignal_injetado"] = True

# --- 3. IMPORTS DO PROJETO ---
from infrastructure.repositories.candidato_repository import CandidatoRepository
from infrastructure.external_api.linkedin.linkedin_service import LinkedInService
from application.services.registrar_candidato_service import RegistrarCandidatoService
from ui.app_view import renderizar_interface

# --- 4. LÓGICA DO APP ---
repo = CandidatoRepository()
auth = LinkedInService(
    client_id=st.secrets["LINKEDIN_CLIENT_ID"],
    client_secret=st.secrets["LINKEDIN_CLIENT_SECRET"],
    redirect_uri=st.secrets["REDIRECT_URI"]
)
service = RegistrarCandidatoService(repo, auth)

# Chama a interface por último
renderizar_interface(service, auth)