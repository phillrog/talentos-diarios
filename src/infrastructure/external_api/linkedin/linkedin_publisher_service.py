import requests
import os
from application.interfaces.ipublicador_service import IPublicadorService

class LinkedInPublisherService(IPublicadorService):
    def __init__(self, access_token: str, organization_id: str):
        self.access_token = access_token
        self.author_urn = f"urn:li:organization:{organization_id}"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }

    def postar(self, caminho_pdf: str, titulo_post: str):
        url = "https://api.linkedin.com/v2/ugcPosts"
        data = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": "TESTE"},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        response = requests.post(url, headers=self.headers, json=data)
        print(response)