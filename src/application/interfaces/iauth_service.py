from abc import ABC, abstractmethod

class IAuthService(ABC):
    @abstractmethod
    def obter_url_login(self) -> str: pass

    @abstractmethod
    def obter_token_acesso(self, codigo_autorizacao: str) -> str: pass

    @abstractmethod
    def obter_dados_perfil(self, token: str) -> dict: pass