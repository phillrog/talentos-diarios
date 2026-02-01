from abc import ABC, abstractmethod
from typing import List
from domain.entities.candidato import Candidato

class ICandidatoRepository(ABC):
    @abstractmethod
    def salvar(self, candidato: Candidato): pass
    
    def salvar_no_github(self, candidato: Candidato): pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Candidato]: pass

    @abstractmethod
    def remover(self, urn_id: str): pass