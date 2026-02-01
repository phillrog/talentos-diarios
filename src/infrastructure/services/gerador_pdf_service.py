import locale
import base64
import os
from io import BytesIO
from PIL import Image, ImageOps, ImageDraw
from fpdf import FPDF
from datetime import datetime
from application.interfaces.idocumento_service import IDocumentoService

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    locale.setlocale(locale.LC_TIME, 'portuguese_brazil')

class GeradorPDFService(IDocumentoService):
    def gerar(self, candidatos: list):
        # Paleta Dark Tech
        COLOR_BG = (34, 40, 49)      # #222831
        COLOR_CARD = (57, 62, 70)    # #393E46
        COLOR_ACCENT = (0, 173, 181) # #00ADB5
        COLOR_TEXT = (238, 238, 238) # #EEEEEE

        class PDF(FPDF):
            def footer(self):
                # Mensagem de instrução para LinkedIn
                self.set_y(-15)
                self.set_font("Helvetica", 'I', 12)
                self.set_text_color(*COLOR_ACCENT)
                self.cell(0, 5, "Arraste para o lado para ver mais profissionais >>>", align='C', ln=True)
                
                # Numeração da Página
                self.set_font("Helvetica", 'I', 8)
                self.set_text_color(100, 100, 100)
                self.cell(0, 5, f"Página {self.page_no()} de {{nb}}", align='C')
        pdf = PDF(orientation='P', unit='mm', format=(200, 200))
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.alias_nb_pages() # Para o total de páginas {nb}
        
        agora = datetime.now()
        data_atual = agora.strftime("%d DE %B DE %Y").upper()
        total_talentos = len(candidatos)

        def adicionar_estilo_base():
            # Fundo Principal
            pdf.set_fill_color(*COLOR_BG)
            pdf.rect(0, 0, 200, 200, 'F')
            
            #  Moldura Externa da Página
            pdf.set_draw_color(57, 62, 70)
            pdf.set_line_width(0.3)
            pdf.rect(5, 5, 190, 190, 'D') # Moldura a 5mm da borda
            
            # Círculo decorativo mantido
            pdf.set_draw_color(45, 50, 58)
            pdf.ellipse(120, -20, 100, 100, 'D')

        def adicionar_cabecalho(is_first=False):
            # --- ÁREA DO TÍTULO E LOGO ---
            pdf.set_font("Helvetica", 'B', 20)
            pdf.set_text_color(*COLOR_TEXT)
            pdf.set_xy(15, 10)
            pdf.cell(40, 10, "TALENTOS", align='L')
            pdf.set_text_color(*COLOR_ACCENT)
            pdf.cell(40, 10, "DIÁRIOS", align='L')

            # Linha vertical divisória ao lado do título
            pdf.set_draw_color(*COLOR_ACCENT)
            pdf.set_line_width(0.5)
            pdf.line(100, 11, 100, 19)
            
            pdf.set_xy(105, 13)
            pdf.set_font("Helvetica", 'B', 12)
            pdf.set_text_color(*COLOR_ACCENT)
            pdf.cell(0, 5, "NOVO DIÁRIO PUBLICADO!", ln=True)

            # Logo
            try:
                dir_atual = os.path.dirname(os.path.abspath(__file__))
                caminho_logo = os.path.normpath(os.path.join(dir_atual, "..", "..", "assets", "images", "logo.png"))
                if os.path.exists(caminho_logo):
                    img = Image.open(caminho_logo).convert("RGBA")
                    tamanho = min(img.size)
                    img = ImageOps.fit(img, (tamanho, tamanho), centering=(0.5, 0.5))
                    mask = Image.new('L', img.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0) + img.size, fill=255)
                    logo_round = Image.new("RGB", img.size, COLOR_BG)
                    logo_round.paste(img, mask=mask)
                    pdf.image(logo_round, x=170, y=6.5, w=14)
            except: pass
            
            # --- LINHAS ESTRUTURAIS ---
            pdf.set_draw_color(*COLOR_CARD)
            pdf.set_line_width(0.2)
            

            pdf.set_xy(15, 25)
            pdf.set_font("Helvetica", '', 12)
            pdf.set_text_color(180, 180, 180)
            pdf.cell(0, 4, f"Apresentamos {total_talentos} profissionais qualificados para sua empresa.", ln=True)
            

            pdf.set_draw_color(*COLOR_CARD)
                
            pdf.line(15, 22, 185, 22)

        # Configurações do Grid ajustadas para caber 6 na primeira página
        cards_por_pagina = 6
        colunas = 3
        largura_card = 56
        altura_card = 70 
        x_inicial = 14
        y_primeira_pagina = 35 # Espaço para o cabeçalho maior
        y_outras_paginas = 35
        espacamento_x = 4
        espacamento_y = 4

        chunks = [candidatos[i:i + cards_por_pagina] for i in range(0, len(candidatos), cards_por_pagina)]

        for p_idx, grupo in enumerate(chunks):
            pdf.add_page()
            adicionar_estilo_base()
            
            is_first = (p_idx == 0)
            adicionar_cabecalho(is_first=is_first)
            
            y_offset = y_primeira_pagina if is_first else y_outras_paginas

            for i, c in enumerate(grupo):
                col = i % colunas
                row = i // colunas
                x = x_inicial + (col * (largura_card + espacamento_x))
                y = y_offset + (row * (altura_card + espacamento_y))
                
                # Card
                pdf.set_fill_color(*COLOR_CARD)
                pdf.rect(x, y, largura_card, altura_card, 'F')
                
                # --- CABEÇALHO DO CARD ---
                pdf.set_fill_color(45, 50, 58)
                altura_bloco_header = 16
                pdf.rect(x, y, largura_card, altura_bloco_header, 'F')
                
                pdf.set_font("Helvetica", 'B', 8)
                pdf.set_text_color(*COLOR_ACCENT)
                
                # Cargo
                texto_cargo = c['cargo'][:80].upper()
                largura_util = largura_card - 4
                altura_linha = 3.5
                
                # Calcular largura real para saber o número de linhas exato
                largura_texto_total = pdf.get_string_width(texto_cargo)
                import math
                num_linhas = math.ceil(largura_texto_total / largura_util)
                
                # Se o texto for muito longo  limita a altura
                altura_total_texto = num_linhas * altura_linha
                
                # LÓGICA DE ALINHAMENTO DINÂMICO:
                # Se tiver 1 linha: Fica no centro perfeito.
                # Se tiver mais linhas: O offset diminui proporcionalmente para o topo.
                if num_linhas == 1:
                    offset_vertical = (altura_bloco_header - altura_total_texto) / 2
                else:
                    # offset menor)
                    offset_vertical = (altura_bloco_header - altura_total_texto) * 0.4 
                
                pdf.set_xy(x + 2, y + max(1, offset_vertical))
                pdf.multi_cell(largura_util, altura_linha, texto_cargo, align='J')
                
                # --- CORPO DO CARD (BORDA AO REDOR DA FOTO E NOME) ---
                pdf.set_draw_color(80, 85, 90) 
                pdf.set_line_width(0.2)                
                pdf.rect(x + 2, y + 18, largura_card - 4, altura_card - 28, 'D')

                # Foto 
                if c.get('foto'):
                    try:
                        img_str = c['foto'].split(",")[1] if "," in c['foto'] else c['foto']
                        img_data = base64.b64decode(img_str)
                        img_pill = Image.open(BytesIO(img_data)).convert("RGBA")
                        img_pill = ImageOps.fit(img_pill, (200, 200), centering=(0.5, 0.5))
                        mask = Image.new('L', img_pill.size, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0, 200, 200), fill=255)
                        img_circ = Image.new("RGB", img_pill.size, COLOR_CARD)
                        img_circ.paste(img_pill, mask=mask)

                        pdf.image(img_circ, x=x+18, y=y+21, w=20)
                    except: pass

                # Nome
                pdf.set_xy(x + 3, y + 43)
                pdf.set_font("Helvetica", 'B', 11)
                pdf.set_text_color(*COLOR_TEXT)
                pdf.multi_cell(largura_card - 6, 4.5, c['nome'].title(), align='C')

                # Botão
                pdf.set_fill_color(*COLOR_ACCENT)
                pdf.rect(x + 2, y + altura_card - 8, 52, 5, 'F')
                pdf.set_xy(x, y + altura_card - 8)
                pdf.set_font("Helvetica", 'B', 10)
                pdf.set_text_color(*COLOR_BG)
                pdf.cell(largura_card, 5, "VER PERFIL", link=c['perfil_url'], align='C')

        pdf.output("./src/static/talentos_diarios.pdf")
        print("✅ PDF ajustado com paginação e grid corrigido!")