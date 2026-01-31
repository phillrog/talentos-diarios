from abc import ABC, abstractmethod


class IPublicadorService(ABC):
    @abstractmethod
    def postar(self, candidatos: list):
        pass