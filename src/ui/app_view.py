import streamlit as st
import os
import urllib.parse

from ui.helpers import get_base64_of_bin_file
from ui.styles import get_custom_css, get_footer_html

def renderizar_interface(registrar_service, auth_service):
    # 1. Configuração Inicial da Página
    st.set_page_config(
        page_title="Talentos Diários", 
        page_icon="📰", 
        layout="wide"
    )

    # 2. Processamento de Ativos (Logo)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGO_PATH = os.path.join(BASE_DIR, "assets", "images", "logo.png")
    
    logo_b64 = get_base64_of_bin_file(LOGO_PATH)
    logo_html = f'data:image/png;base64,{logo_b64}' if logo_b64 else ""

    # 3. Injeção de CSS e Cabeçalho Customizado
    # Importado de assets/styles.py
    st.markdown(get_custom_css(logo_html), unsafe_allow_html=True)

    # 4. Lógica de Callback do LinkedIn
    params = st.query_params
    if "code" in params:
        with st.spinner("🚀 Finalizando seu registro..."):
            try:
                codigo = params["code"]
                state_raw = params.get("state", "")
                state_decoded = urllib.parse.unquote(state_raw)
                
                # Extração segura do cargo e link
                if "-*-" in state_decoded:
                    cargo_rec, link_rec = state_decoded.split("-*-", 1)
                else:
                    cargo_rec, link_rec = state_decoded, ""
                
                candidato = registrar_service.executar(codigo, cargo_rec, link_rec)
                st.balloons()
                st.success(f"✅ Sucesso! {candidato.nome} já está na vitrine.")
                st.query_params.clear()
            except Exception as e:
                st.error(f"Erro no registro: {e}")

    # 5. Estrutura do Formulário (Centralizado)
    # Proporção [1, 1.8, 1] para manter o card imponente no centro
    col_space1, col_form, col_space2 = st.columns([1, 1.8, 1])

    with col_form:
        # Container com bordas arredondadas (estilizado via CSS)
        with st.container(border=True):

            cargo_digitado = st.text_input(
                "Qual seu cargo ou especialidade?", 
                placeholder="Ex: C# | Fullstack Developer | .NET",
                key="cargo_usuario"
            )
            
            link_perfil = st.text_input(
                "Cole o link do seu perfil do LinkedIn", 
                placeholder="https://www.linkedin.com/in/seu-perfil"
            )
            
            st.write("") # Espaçador visual interno
            
            # Lógica do Botão de Ação
            if cargo_digitado and link_perfil:
                url_final = auth_service.obter_url_login(cargo_digitado, link_perfil)
                st.link_button("REGISTRAR COM LINKEDIN", url_final, use_container_width=True)
                st.markdown('<p style="text-align: center; color: #46556a; font-size: 0.85rem; margin-top: 15px; font-weight: 600;">'
                            '🔒 Conexão segura via API oficial</p>', unsafe_allow_html=True)
            else:
                st.button("REGISTRAR COM LINKEDIN", use_container_width=True, disabled=True)
                st.info("Preencha os campos acima para continuar.")
                
            st.markdown("""
                <div class="vitrine-link-container">
                    <a href="https://talentos-diarios-portal.vercel.app" target="_blank" class="vitrine-link">
                        🔍 Clique aqui para visualizar a vitrine
                    </a>
                </div>
            """, unsafe_allow_html=True)

    # 6. Rodapé e Finalização
    st.write("")
    st.divider()
    
    # Rodapé Estilizado (Importado de assets/styles.py)
    st.markdown(get_footer_html(), unsafe_allow_html=True)

    # Opção de Gerenciamento
    st.markdown("""
            <div class="disclaimer-box">
                <p class="disclaimer-text">
                    <b>💡 Disclaimer:</b> Este projeto é uma iniciativa de estudo e portfólio. 
                    O cadastro e a exibição na vitrine visam complementar sua visibilidade, 
                    não garantindo contratações ou propostas.
                </p>
            </div>
        """, unsafe_allow_html=True)