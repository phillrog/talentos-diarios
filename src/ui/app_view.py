import streamlit as st
import os
import urllib.parse
import base64
from ui.helpers import get_base64_of_bin_file
from ui.styles import get_custom_css, get_footer_html

def renderizar_interface(registrar_service, auth_service):
    # 1. Configuração Inicial
    st.set_page_config(
        page_title="Talentos Diários", 
        page_icon="👔", 
        layout="wide"
    )

    # 2. Caminhos de Imagens
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGO_PATH = os.path.join(BASE_DIR, "assets", "images", "logo.png")
    LINKEDIN_ICON_PATH = os.path.join(BASE_DIR, "assets", "images", "linkedin.svg")
    
    # 3. Processamento de Logos e Ícones
    logo_b64 = get_base64_of_bin_file(LOGO_PATH)
    logo_html = f'data:image/png;base64,{logo_b64}' if logo_b64 else ""
    
    linkedin_b64 = get_base64_of_bin_file(LINKEDIN_ICON_PATH)
    linkedin_icon_data = f'data:image/svg+xml;base64,{linkedin_b64}' if linkedin_b64 else ""

    # 4. Injeção de CSS
    st.markdown(get_custom_css(logo_html), unsafe_allow_html=True)

    # 5. Callback LinkedIn (Mantido original)
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

    # 6. Formulário Centralizado
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
            
            # 7. Botão Customizado com Ícone LinkedIn
            if cargo_digitado and link_perfil:
                url_final = auth_service.obter_url_login(cargo_digitado, link_perfil)
                
                st.markdown(f"""
                    <a href="{url_final}" target="_top" style="text-decoration: none;">
                        <div id="linkedin-button"
                            style="
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            gap: 10px;
                            background-color: #0077b5;
                            color: white;
                            padding: 12px 20px;
                            border-radius: 8px;
                            font-weight: 700;
                            font-size: 0.9rem;
                            transition: background-color 0.3s;
                            border: none;
                            cursor: pointer;
                            width: 100%;
                            text-align: center;
                            box-sizing: border-box;
                        "
                        >                            
                            Cadastrar via <img src="{linkedin_icon_data}" width="64" height="24" style="filter: brightness(0) invert(1);">
                        </div>
                    </a>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div
                        onmouseover="this.style.backgroundColor='#005a87'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 15px rgba(0,0,0,0.2)';" 
                        onmouseout="this.style.backgroundColor='#0077b5'; this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)';" 
                        style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                        background-color: #e2e8f0;
                        color: #94a3b8;
                        padding: 12px 20px;
                        border-radius: 8px;
                        font-weight: 700;
                        font-size: 0.9rem;
                        width: 100%;
                        cursor: not-allowed;
                        box-sizing: border-box;
                    ">
                        Cadastrar via <img src="{linkedin_icon_data}" width="64" height="24" style="filter: brightness(0) invert(1);">
                    </div>
                """, unsafe_allow_html=True)
                st.caption("Preencha os campos para continuar.")
                
            st.markdown(f"""
                <div style="text-align: center; margin-top: 20px;">
                    <a href="https://talentos-diarios-portal.vercel.app" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: 600; font-size: 0.9rem;">
                        🔍 Ver vitrine de candidatos disponíveis
                    </a>
                </div>
            """, unsafe_allow_html=True)

    # 8. Rodapé e Disclaimer
    st.markdown(get_footer_html(), unsafe_allow_html=True)
    st.markdown("""
        <div class="disclaimer-box">
            <p class="disclaimer-text">
                <b>💡 Nota:</b> Este é um projeto de portfólio. O cadastro aumenta sua visibilidade, 
                mas não garante contratação direta.
            </p>
        </div>
    """, unsafe_allow_html=True)