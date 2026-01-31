from abc import ABC, abstractmethod


class IDocumentoService(ABC):
    @abstractmethod
    def gerar(self, candidatos: list):
        pass