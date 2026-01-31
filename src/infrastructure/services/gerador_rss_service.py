from feedgen.feed import FeedGenerator

from application.interfaces.idocumento_service import IDocumentoService

class GeradorRSSService(IDocumentoService):
    def gerar(self, candidatos: list):
        fg = FeedGenerator()
        fg.title('Talentos Diários')
        fg.link(href='http://localhost:8501', rel='alternate')
        fg.description('Feed de talentos atualizado')

        for c in candidatos:
            fe = fg.add_entry()
            fe.title(f"{c['cargo']} - {c['nome']}")
            fe.link(href=c['perfil_url'])
            
        fg.rss_file('feed.xml')
        print("✅ RSS Gerado com sucesso.")