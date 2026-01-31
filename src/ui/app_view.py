import streamlit as st
import urllib.parse

def renderizar_interface(registrar_service, auth_service):
    st.set_page_config(page_title="Talentos Diários", page_icon="📰")

    st.title("📰 Talentos Diários")
    st.subheader("Sua vitrine diária para o mercado de trabalho")

    # Verificação de Retorno do LinkedIn (Callback)
    params = st.query_params
    
    if "code" in params:
        with st.spinner("Finalizando seu registro..."):
            try:
                codigo = params["code"]
                state_enc = params.get("state", "")
                
                state_decoded = urllib.parse.unquote(state_enc)
                if "-*-" in state_decoded:
                    cargo_recuperado, link_recuperado = state_decoded.split("-*-", 1)
                else:
                    cargo_recuperado = state_decoded or "Profissional"
                    link_recuperado = ""                    
                
                candidato = registrar_service.executar(codigo, cargo_recuperado, link_recuperado)
                
                st.success(f"✅ Sucesso! {candidato.nome} registrado como **{cargo_recuperado}** e com o perfil **{link_recuperado}** .")
                st.balloons()
                st.query_params.clear()
            except Exception as e:
                st.error(f"Erro no registro: {e}")

    # Área de Registro
    with st.container(border=True):
        st.write("### 🚀 Apareça no próximo jornal")
        
        cargo_digitado = st.text_input(
            "Qual seu cargo ou especialidade?", 
            placeholder="Ex: C# | Fullstack Developer | .NET | Angular | Cloud & IA | Analista de Sistemas",
            key="cargo_usuario"
        )
        
        link_perfil = st.text_input("Cole o link do seu perfil do LinkedIn", placeholder="https://www.linkedin.com/in/seu-perfil")
        
        # LÓGICA DE REDIRECIONAMENTO 
        if cargo_digitado and link_perfil:
            url_final = auth_service.obter_url_login(cargo_digitado, link_perfil)            
            st.markdown(f"""
                <a href="{url_final}" target="_self" style="text-decoration: none;">
                    <div style="
                        background-color: #ff4b4b; 
                        color: white; 
                        padding: 0.5rem 1rem; 
                        text-align: center; 
                        border-radius: 0.5rem; 
                        font-family: sans-serif;
                        font-weight: 500;
                        cursor: pointer;
                        border: 1px solid #ff4b4b;
                        transition: opacity 0.2s;
                    " onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">
                        🚀 Confirmar Registro com LinkedIn
                    </div>
                </a>
            """, unsafe_allow_html=True)
        else:
            st.button("Entrar com LinkedIn", use_container_width=True, disabled=True)
            st.caption("Preencha os campos acima para liberar o acesso.")
    
    with st.expander("❌ Remover perfil"):
        st.write("Remova o acesso da aplicação no seu LinkedIn.")
    
    st.divider()
    st.caption("Conectado com API oficial do LinkedIn.")