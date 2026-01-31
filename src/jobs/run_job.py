from application.services.gerenciador_candidatos_service import GerenciadorCandidatosService
from application.services.jornal_diario_service import JornalDiarioService
from infrastructure.services.gerador_pdf_service import GeradorPDFService
from infrastructure.services.gerador_rss_service import GeradorRSSService


if __name__ == "__main__":
    # Injeção de Dependência para o Robô
    repo = GerenciadorCandidatosService('candidatos.json')
    saidas = [GeradorPDFService(), GeradorRSSService()]
    
    # Orquestração
    app = JornalDiarioService(repo, saidas)
    app.processar_edicao_do_dia()