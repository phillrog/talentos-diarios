from typing import List
from domain.entities.candidato import Candidato
from domain.interfaces.icandidato_repository import ICandidatoRepository


class GerenciadorCandidatosService:
    def __init__(self, repositorio: ICandidatoRepository):
        # Agora o serviço depende da interface do repositório
        self.repositorio = repositorio

    def obter_candidatos_validos(self) -> List[Candidato]:
        """
        Retorna a lista de candidatos convertida em objetos de domínio.
        A lógica de filtro de 30 dias já está embutida no buscar_todos() do repositório.
        """
        try:
            # O repositório já cuida de ler e filtrar os últimos 30 dias
            candidatos = self.repositorio.buscar_todos()
            return candidatos
        except Exception as e:
            # Log de erro ou tratamento específico
            print(f"Erro ao obter candidatos: {e}")
            return []