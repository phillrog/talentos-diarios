from application.interfaces.idocumento_service import IDocumentoService
from application.services.gerenciador_candidatos_service import GerenciadorCandidatosService


class JornalDiarioService:
    def __init__(self, gerenciador: GerenciadorCandidatosService, geradores: list[IDocumentoService]):
        self.gerenciador = gerenciador
        self.geradores = geradores

    def processar_edicao_do_dia(self):
        # Busca quem está no JSON e remove os antigos (+30 dias)
        candidatos = self.gerenciador.obter_candidatos_validos()
        if not candidatos:
            print("Aviso: Nenhum candidato para processar.")
            return

        for gerador in self.geradores:
            gerador.gerar(candidatos)     