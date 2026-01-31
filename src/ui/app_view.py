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
                if "|" in state_decoded:
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
        if st.button("Entrar com LinkedIn", use_container_width=True):
            if not cargo_digitado:
                st.warning("Por favor, digite seu cargo antes de prosseguir.")
            if not link_perfil:
                st.warning("Por favor, digite link do seu perfil linkedin.")
            else:
                url_final = auth_service.obter_url_login(cargo_digitado, link_perfil)
                
                # Redirecionamento via HTML (Força a saída da página levando os dados)
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{url_final}\'">', unsafe_allow_html=True)
    
    with st.expander("❌ Remover perfil"):
        st.write("Remova o acesso da aplicação no seu LinkedIn.")
    
    st.divider()
    st.caption("Conectado com API oficial do LinkedIn.")