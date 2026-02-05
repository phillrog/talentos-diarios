import requests

from application.interfaces.iauth_service import IAuthService


class LinkedInService(IAuthService):
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        self.user_info_url = "https://api.linkedin.com/v2/userinfo" # API V2 para dados básicos

    def obter_url_login(self, cargo="", link_perfil="") -> str:
        state_combinado = f"{cargo}-*-{link_perfil}"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid profile",
            "state": state_combinado
        }
        request_url = requests.Request("GET", self.auth_url, params=params).prepare().url
        return request_url

    def obter_token_acesso(self, codigo_autorizacao: str) -> str:
        data = {
            "grant_type": "authorization_code",
            "code": codigo_autorizacao,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        return response.json().get("access_token")

    def obter_dados_perfil(self, token: str, link_perfil: str) -> dict:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.user_info_url, headers=headers)
        response.raise_for_status()
        dados = response.json()
        
        return {
            "urn_id": dados.get("sub"), # O ID único no OpenID
            "nome": f"{dados.get('given_name')} {dados.get('family_name')}",
            "perfil_url": link_perfil.lower(),
            "foto": dados.get("picture")
        }