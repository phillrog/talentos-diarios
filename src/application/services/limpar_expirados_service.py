

from infrastructure.repositories.candidato_repository import CandidatoRepository


class LimparCandidatosExpiradosService:
    def __init__(self, repo: CandidatoRepository):
        self.repo = repo

    def executar(self):
        candidatos = self.repo.buscar_todos()
        for c in candidatos:
            if c.esta_expirado():
                self.repo.remover(c.urn_id)