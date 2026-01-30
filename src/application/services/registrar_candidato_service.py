from datetime import datetime

from application.interfaces.iauth_service import IAuthService
from domain.entities.candidato import Candidato
from domain.interfaces.icandidato_repository import ICandidatoRepository

class RegistrarCandidatoService:
    def __init__(self, repo: ICandidatoRepository, auth_service: IAuthService):
        self.repo = repo
        self.auth_service = auth_service

    def executar(self, codigo_autorizacao: str, cargo_informado: str):
        # Troca o código pelo Token
        token = self.auth_service.obter_token_acesso(codigo_autorizacao)
        
        # Pega os dados do perfil
        perfil = self.auth_service.obter_dados_perfil(token)
        
        # Cria a entidade
        novo_candidato = Candidato(
            urn_id=perfil['urn_id'],
            nome=perfil['nome'],
            cargo=cargo_informado, # O cargo a pessoa digita no Streamlit
            perfil_url=perfil['perfil_url'],
            access_token=token,
            data_cadastro=datetime.now()
        )
        
        # Salva no JSON via Repositório
        self.repo.salvar(novo_candidato)
        return novo_candidato