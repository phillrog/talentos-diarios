import json
import os
from typing import List
from domain.entities.candidato import Candidato
from domain.interfaces.icandidato_repository import ICandidatoRepository



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