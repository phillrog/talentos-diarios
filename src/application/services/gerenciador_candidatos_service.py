import json
import os
from datetime import datetime, timedelta

class GerenciadorCandidatosService:
    def __init__(self, caminho_json):
        self.caminho_json = caminho_json

    def obter_candidatos_validos(self, dias=30):
        if not os.path.exists(self.caminho_json):
            return []
        
        with open(self.caminho_json, 'r', encoding='utf-8') as f:
            candidatos = json.load(f)
        
        hoje = datetime.now()
        validos = [
            c for c in candidatos 
            if hoje - datetime.fromisoformat(c['data_cadastro']) < timedelta(days=dias)
        ]
        return validos