import base64
from datetime import datetime
import requests
from application.interfaces.iauth_service import IAuthService
from domain.entities.candidato import Candidato
from domain.interfaces.icandidato_repository import ICandidatoRepository

class RegistrarCandidatoService:
    def __init__(self, repo: ICandidatoRepository, auth_service: IAuthService):
        self.repo = repo
        self.auth_service = auth_service
        
    def _converter_imagem_para_base64(self, url_foto: str) -> str:
        if not url_foto:
            return None
        try:
            response = requests.get(url_foto, timeout=10)
            if response.status_code == 200:
                img_base64 = base64.b64encode(response.content).decode('utf-8')
                return f"data:image/jpeg;base64,{img_base64}"
        except Exception as e:
            print(f"Erro ao baixar foto: {e}")
        return None

    def executar(self, codigo_autorizacao: str, cargo_informado: str, link_perfil: str) -> Candidato:
        # Troca o código pelo Token
        token = self.auth_service.obter_token_acesso(codigo_autorizacao)
        
        # Pega os dados do perfil
        perfil = self.auth_service.obter_dados_perfil(token, link_perfil)
        
        # Converte a foto para base64
        foto_base64 = self._converter_imagem_para_base64(perfil['foto'])
        
        # Cria a entidade
        novo_candidato = Candidato(
            nome=perfil['nome'],
            cargo=cargo_informado, # O cargo a pessoa digita no Streamlit
            perfil_url=perfil['perfil_url'],
            data_cadastro=datetime.now(),
            foto=foto_base64
        )
        
        # Salva no JSON via Repositório
        self.repo.salvar(novo_candidato)
        return novo_candidato