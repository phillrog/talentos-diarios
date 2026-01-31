from application.interfaces.idocumento_service import IDocumentoService
from application.interfaces.ipublicador_service import IPublicadorService
from application.services.gerenciador_candidatos_service import GerenciadorCandidatosService


class JornalDiarioService:
    def __init__(self, gerenciador: GerenciadorCandidatosService, geradores: list[IDocumentoService], publicador: IPublicadorService=None):
        self.gerenciador = gerenciador
        self.geradores = geradores
        self.publicador = publicador
        
    def processar_edicao_do_dia(self):
        # Busca quem está no JSON e remove os antigos (+30 dias)
        candidatos = self.gerenciador.obter_candidatos_validos()
        if not candidatos:
            print("Aviso: Nenhum candidato para processar.")
            return

        for gerador in self.geradores:
            gerador.gerar(candidatos)     
            
        if self.publicador:
            print("Iniciando publicação no LinkedIn...")
            # Aqui passamos o caminho do PDF que acabou de ser gerado
            self.publicador.postar("jornal_do_dia.pdf", "Edição diária da Gazeta do Talento")