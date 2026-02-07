import streamlit as st
import os
import urllib.parse
from ui.helpers import get_base64_of_bin_file
from ui.styles import get_custom_css, get_footer_html

def renderizar_interface(registrar_service, auth_service):
    # 1. Configuração Inicial
    st.set_page_config(
        page_title="Talentos Diários", 
        page_icon="👔", 
        layout="wide"
    )

    # 2. Logo
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGO_PATH = os.path.join(BASE_DIR, "assets", "images", "logo.png")
    logo_b64 = get_base64_of_bin_file(LOGO_PATH)
    logo_html = f'data:image/png;base64,{logo_b64}' if logo_b64 else ""

    # 3. Injeção de CSS
    st.markdown(get_custom_css(logo_html), unsafe_allow_html=True)

    # 4. Callback LinkedIn (Mantido original)
    params = st.query_params
    if "code" in params:
        with st.spinner("🚀 Finalizando seu registro..."):
            try:
                codigo = params["code"]
                state_raw = params.get("state", "")
                state_decoded = urllib.parse.unquote(state_raw)
                cargo_rec, link_rec = state_decoded.split("-*-", 1) if "-*-" in state_decoded else (state_decoded, "")
                
                candidato = registrar_service.executar(codigo, cargo_rec, link_rec)
                st.balloons()
                st.success(f"✅ Sucesso! {candidato.nome} já está na vitrine.")
                st.query_params.clear()
            except Exception as e:
                st.error(f"Erro no registro: {e}")

    # 5. Formulário Centralizado
    _, col_form, _ = st.columns([1, 1.5, 1])

    with col_form:
        with st.container(border=True):
            st.subheader("Cadastro de Candidato")
            
            cargo_digitado = st.text_input(
                "Qual seu cargo ou especialidade?", 
                placeholder="Ex: Desenvolvedor .NET | Designer UX",
                key="cargo_usuario"
            )
            
            link_perfil = st.text_input(
                "Link do seu perfil do LinkedIn", 
                placeholder="https://www.linkedin.com/in/seu-perfil"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if cargo_digitado and link_perfil:
                url_final = auth_service.obter_url_login(cargo_digitado, link_perfil)
                st.link_button("CADASTRAR VIA LINKEDIN", url_final, use_container_width=True)
            else:
                st.button("CADASTRAR VIA LINKEDIN", use_container_width=True, disabled=True)
                st.caption("Preencha os campos para continuar.")
                
            st.markdown(f"""
                <div style="text-align: center; margin-top: 20px;">
                    <a href="https://talentos-diarios-portal.vercel.app" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: 600; font-size: 0.9rem;">
                        🔍 Ver vitrine de candidatos disponíveis
                    </a>
                </div>
            """, unsafe_allow_html=True)

    # 6. Rodapé e Disclaimer
    st.markdown(get_footer_html(), unsafe_allow_html=True)
    st.markdown("""
        <div class="disclaimer-box">
            <p class="disclaimer-text">
                <b>💡 Nota:</b> Este é um projeto de portfólio. O cadastro aumenta sua visibilidade, 
                mas não garante contratação direta.
            </p>
        </div>
    """, unsafe_allow_html=True)