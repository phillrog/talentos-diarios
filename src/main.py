import streamlit as st
from application.services.registrar_candidato_service import RegistrarCandidatoService
from infrastructure.external_api.linkedin.linkedin_service import LinkedInService
from infrastructure.repositories.candidato_repository import CandidatoRepository


# --- Configuração de Estilo ---
st.set_page_config(page_title="Gazeta do Talento", page_icon="📰")

# --- Injeção de Dependência (SOLID) ---
# Aqui carregamos as configurações sensíveis de forma segura
repo = CandidatoRepository()
auth_service = LinkedInService(
    client_id=st.secrets["LINKEDIN_CLIENT_ID"],
    client_secret=st.secrets["LINKEDIN_CLIENT_SECRET"],
    redirect_uri=st.secrets["REDIRECT_URI"]
)
registrar_use_case = RegistrarCandidatoService(repo, auth_service)

# --- Lógica da Interface ---
st.title("📰 Gazeta do Talento")
st.subheader("Sua vitrine diária para o mercado de trabalho")

# 1. Verificação de Retorno do LinkedIn (Callback)
query_params = st.query_params
if "code" in query_params:
    with st.spinner("Autenticando com o LinkedIn..."):
        try:
            # Pegamos o código da URL e o cargo que a pessoa quer exibir
            codigo = query_params["code"]
            cargo = st.session_state.get('cargo_input', 'Profissional em Busca de Oportunidades')
            
            candidato = registrar_use_case.executar(codigo, cargo)
            st.success(f"Parabéns, {candidato.nome}! Você está na fila do Jornal.")
            st.balloons()
            # Limpa o código da URL para evitar re-processamento
            st.query_params.clear()
        except Exception as e:
            st.error(f"Erro ao registrar: {e}")

# 2. Área de Registro
with st.container(border=True):
    st.write("### 🚀 Quer aparecer no próximo jornal?")
    st.write("Logue com seu LinkedIn. Seus dados serão exibidos por 30 dias.")
    
    cargo_input = st.text_input("Qual seu cargo ou especialidade?", placeholder="Ex: Desenvolvedor Python Pleno")
    st.session_state['cargo_input'] = cargo_input

    # O botão não pede senha, ele apenas redireciona para o LinkedIn
    url_login = auth_service.obter_url_login()
    st.link_button("Entrar com LinkedIn", url_login, use_container_width=True)

# 3. Área de Desinscrição (Revogação)
with st.expander("❌ Deseja remover seu perfil do jornal?"):
    st.write("Basta remover a permissão desta aplicação nas configurações do seu LinkedIn. "
             "Nosso sistema detectará automaticamente e removerá seus dados na próxima atualização.")

# 4. Rodapé Informativo
st.divider()
st.caption("Nota: Seus dados de login permanecem seguros no LinkedIn. "
           "Nós apenas recebemos sua autorização para exibir seu perfil público.")