import streamlit as st
import urllib.parse
import streamlit.components.v1 as components

components.html(
    """
    <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
    <script>
      window.OneSignalDeferred = window.OneSignalDeferred || [];
      OneSignalDeferred.push(async function(OneSignal) {
        await OneSignal.init({
          appId: "66267c67-6b67-4742-a72d-25c884d2fe17",
          notifyButton: {
            enable: true, # Isso vai mostrar o "Sininho" vermelho no canto
          },
          serviceWorkerParam: { scope: "/" },
          serviceWorkerPath: "static/OneSignalSDKWorker.js",
        });
      });
    </script>
    """,
    height=0, # Deixamos altura 0 para o script rodar escondido
)

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
            st.link_button("Entrar com LinkedIn", url_final, use_container_width=True)            
            st.info("Clique no botão acima para autorizar via LinkedIn.")
        else:
            st.button("Entrar com LinkedIn", use_container_width=True, disabled=True)
            st.caption("Preencha os campos acima para liberar o acesso.")
    
    with st.expander("❌ Remover perfil"):
        st.write("Remova o acesso da aplicação no seu LinkedIn.")
    
    st.divider()
    st.caption("Conectado com API oficial do LinkedIn.")