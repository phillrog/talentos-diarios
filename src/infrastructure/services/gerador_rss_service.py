from feedgen.feed import FeedGenerator
import os
from datetime import datetime
from application.interfaces.idocumento_service import IDocumentoService

class GeradorRSSService(IDocumentoService):
    def gerar(self, candidatos: list):
        base_url = os.getenv('APP_URL', 'http://localhost:8501')
        
        fg = FeedGenerator()
        fg.title('Talentos Diários')
        fg.link(href=base_url, rel='alternate')
        fg.description('Feed de talentos atualizado')

        for c in candidatos:
            fe = fg.add_entry()
            fe.title(f"{c.cargo} - {c.nome}")
            fe.link(href=c.perfil_url)
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            fe.id(f"{c.perfil_url}?v={timestamp}")                         
            
            fe.description(f"Candidato(a) encontrado {c.cargo}. Confira o perfil completo no link.")
            
            fe.pubDate(datetime.now().astimezone())                    
            
        fg.rss_file('./src/static/feed.xml')
        print(f"✅ Gerado com sucesso usando a URL: {base_url}")        