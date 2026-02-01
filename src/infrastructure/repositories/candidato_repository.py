import json
import os
from typing import List
from domain.entities.candidato import Candidato
from domain.interfaces.icandidato_repository import ICandidatoRepository
from github import Github


class CandidatoRepository(ICandidatoRepository):
    def __init__(self, file_path: str = "./src/static/candidatos.json"):
        self.file_path = file_path

    def _ler_arquivo(self) -> list:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def salvar(self, candidato: Candidato):
        candidatos = self._ler_arquivo()

        candidatos = [c for c in candidatos if c['perfil_url'] != candidato.perfil_url]
        candidatos.append(candidato.to_dict())
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=4, ensure_ascii=False)

    def buscar_todos(self) -> List[Candidato]:
        dados = self._ler_arquivo()
        return [Candidato.from_dict(d) for d in dados]

    def remover(self, perfil_url: str):
        candidatos = self._ler_arquivo()
        candidatos = [c for c in candidatos if c['perfil_url'] != perfil_url]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=4, ensure_ascii=False)
            
    def salvar_no_github(self, candidato: Candidato):
        token_github = os.getenv("GITHUB_TOKEN")
        if not token_github:
            raise ValueError("GITHUB_TOKEN não configurado nas variáveis de ambiente.")

        g = Github(token_github)
        repo = g.get_repo("phillrog/talentos-diarios")
        
        contents = repo.get_contents("src/static/candidatos.json")
        lista_candidatos = json.loads(contents.decoded_content.decode('utf-8'))
        novo_candidato_dict = candidato.to_dict()
        
        lista_candidatos = [c for c in lista_candidatos if c['perfil_url'] != candidato.perfil_url]
        lista_candidatos.append(novo_candidato_dict)
        
        repo.update_file(
            contents.path, 
            f"Registro: {candidato.nome}", 
            json.dumps(lista_candidatos, indent=4, ensure_ascii=False), 
            contents.sha
        )