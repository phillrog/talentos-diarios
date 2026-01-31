import locale
import base64
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
        pdf = FPDF(orientation='P', unit='mm', format=(200, 200))
        
        agora = datetime.now()
        data_atual = agora.strftime("%A, %d DE %B DE %Y").upper()
        versao = "EDIÇÃO V.1.0.0"
        total_talentos = len(candidatos)
        
        def adicionar_cabecalho_pagina():
            import os
            # 1. Fundo do papel jornal
            pdf.set_fill_color(252, 251, 247)
            pdf.rect(0, 0, 200, 200, 'F')
            
            titulo = "Talentos Diários"
            pdf.set_font("Times", 'B', 32)
            largura_texto = pdf.get_string_width(titulo)
            largura_logo = 18 
            espacamento_interno = 5 
            
            largura_total_bloco = largura_logo + espacamento_interno + largura_texto
            x_inicio = (200 - largura_total_bloco) / 2
            y_pos = 8 

            # 2. Processar a Logo para ficar REDONDA
            try:
                dir_atual = os.path.dirname(os.path.abspath(__file__))
                caminho_logo = os.path.normpath(os.path.join(dir_atual, "..", "..", "assets", "images", "logo.png"))
                
                if os.path.exists(caminho_logo):
                    # Abre a imagem com Pillow para arredondar
                    img_logo = Image.open(caminho_logo).convert("RGBA")
                    
                    # Torna a logo quadrada (proporção 1:1)
                    tamanho_min = min(img_logo.size)
                    img_logo = ImageOps.fit(img_logo, (tamanho_min, tamanho_min), centering=(0.5, 0.5))
                    
                    # Cria a máscara circular
                    mask = Image.new('L', img_logo.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0) + img_logo.size, fill=255)
                    
                    # Aplica a máscara e coloca fundo cor de papel (para não dar erro de transparência no FPDF)
                    logo_redonda = Image.new("RGB", img_logo.size, (252, 251, 247))
                    logo_redonda.paste(img_logo, mask=mask)
                    
                    # Insere a logo já arredondada no PDF
                    pdf.image(logo_redonda, x=x_inicio, y=y_pos - 2, w=largura_logo)
            except Exception as e:
                print(f"Erro ao arredondar logo: {e}")

            # 3. Título Principal
            pdf.set_text_color(18, 18, 18)
            pdf.set_xy(x_inicio + largura_logo + espacamento_interno, y_pos)
            pdf.cell(largura_texto, 15, titulo, ln=True, align='L')
            
            # 4. Linhas de Estilo
            pdf.set_line_width(0.6)
            pdf.line(14, 28, 191, 28)
            pdf.set_font("Times", 'I', 9)
            pdf.set_xy(0, 29)
            pdf.cell(0, 5, f"{data_atual} | {versao}", ln=True, align='C')
            pdf.line(14, 35, 191, 35)

        # --- 1. CAPA ---
        pdf.add_page()
        adicionar_cabecalho_pagina()
        
        num_texto = str(total_talentos)
                
        pdf.set_font("Times", 'B', 14)
        pdf.set_text_color(100, 100, 100)
        pdf.set_xy(0, 44)
        # O largura '0' faz a célula ocupar toda a largura disponível, permitindo o align='C'
        pdf.cell(0, 10, "TOTAL DE PROFISSIONAIS DISPONÍVEIS HOJE", ln=True, align='C')
    
        
        # 2. Configurações do Número (Badge)
        num_texto = str(total_talentos)
        pdf.set_font("Times", 'B', 28)
        
        # Cálculo para centralizar o retângulo do badge
        largura_num = pdf.get_string_width(num_texto) + 12 # Número + margens laterais
        altura_badge = 14
        x_badge = (200 - largura_num) / 2  # Centralização matemática no papel de 200mm
        y_badge = 66
        
        # 3. Desenhar o Background (Badge)
        pdf.set_fill_color(18, 18, 18)
        pdf.rect(x_badge, y_badge, largura_num, altura_badge, 'F')
        
        # 4. Escrever o Número dentro do Badge (Centralizado)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(x_badge, y_badge)
        pdf.cell(largura_num, altura_badge, num_texto, ln=True, align='C')
        
        # 5. Título Inferior
        pdf.set_xy(0, 90)
        pdf.set_font("Times", 'B', 20)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 15, "OPORTUNIDADES EM DESTAQUE", ln=True, align='C')
        
        pdf.set_font("Times", 'I', 12)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 10, "Arraste para o lado e confira os profissionais >>", ln=True, align='C')

        # --- 2. GRID DE CLASSIFICADOS (6 CARDS POR PÁGINA) ---
        cards_por_pagina = 6
        colunas = 3
        largura_card = 58
        altura_card = 75
        x_inicial = 13
        y_inicial = 38
        espacamento = 2

        chunks = [candidatos[i:i + cards_por_pagina] for i in range(0, len(candidatos), cards_por_pagina)]

        for grupo in chunks:
            pdf.add_page()
            adicionar_cabecalho_pagina()
            
            for i in range(cards_por_pagina):
                col = i % colunas
                row = i // colunas
                
                x = x_inicial + (col * (largura_card + espacamento))
                y = y_inicial + (row * (altura_card + espacamento))
                
                # Borda do Card
                pdf.set_draw_color(150, 150, 150)
                pdf.set_line_width(0.2)
                pdf.rect(x, y, largura_card, altura_card)

                if i < len(grupo):
                    c = grupo[i]
                    # Cabeçalho do Card: CARGO
                    pdf.set_fill_color(240, 240, 240)
                    pdf.rect(x, y, largura_card, 18, 'F')
                    pdf.set_xy(x + 2, y + 4)
                    pdf.set_font("Times", 'B', 8)
                    pdf.set_text_color(40, 40, 40)
                    pdf.multi_cell(largura_card - 4, 4, c['cargo'].upper(), align='C')

                    # --- FOTO EM BASE64 (REDONDA E COM MARGEM) ---
                    # Margem de 3mm após o cabeçalho cinza (y+18+3 = y+21)
                    diametro_foto = 24 
                    x_foto = x + (largura_card - diametro_foto) / 2
                    y_foto = y + 21 
                    
                    if c.get('foto'):
                        try:
                            img_str = c['foto']
                            if "," in img_str:
                                img_str = img_str.split(",")[1]
                            
                            img_data = base64.b64decode(img_str)
                            img_pill = Image.open(BytesIO(img_data)).convert("RGBA")
                            
                            # Mantém a proporção 1:1 para o círculo perfeito
                            tamanho_min = min(img_pill.size)
                            img_pill = ImageOps.fit(img_pill, (tamanho_min, tamanho_min), centering=(0.5, 0.5))
                            
                            # Cria máscara circular
                            mask = Image.new('L', img_pill.size, 0)
                            draw = ImageDraw.Draw(mask)
                            draw.ellipse((0, 0) + img_pill.size, fill=255)
                            
                            # Aplica máscara e converte para RGB com fundo do papel
                            img_circular = Image.new("RGB", img_pill.size, (252, 251, 247))
                            img_circular.paste(img_pill, mask=mask)
                            
                            pdf.image(img_circular, x=x_foto, y=y_foto, w=diametro_foto)
                        except Exception as e:
                            print(f"Erro ao processar imagem de {c['nome']}: {e}")
                            pdf.set_draw_color(230, 230, 230)
                            pdf.rect(x_foto, y_foto, diametro_foto, diametro_foto)
                            
                    # Corpo do Card: NOME (Posicionado logo abaixo da foto circular)
                    pdf.set_xy(x + 2, y + 47) 
                    pdf.set_font("Times", 'B', 11)
                    pdf.set_text_color(0, 0, 0)
                    pdf.multi_cell(largura_card - 4, 5, c['nome'].title(), align='C')
                    
                    # Descrição Curta (Mantido conforme original)
                    pdf.set_font("Times", '', 8)
                    pdf.set_text_color(80, 80, 80)
                    pdf.set_x(x + 2)
                    pdf.ln(2)
                    pdf.set_x(x + 2)
                    pdf.multi_cell(largura_card - 4, 3.5, "Disponível para novas conexões estratégicas.", align='C')

                    # Rodapé: LINK (Mantido conforme original)
                    pdf.set_xy(x, y + altura_card - 10)
                    pdf.set_font("Times", 'B', 7)
                    pdf.set_text_color(0, 0, 255)
                    pdf.cell(largura_card, 10, "PERFIL LINKEDIN", link=c['perfil_url'], border='T', align='C')
                else:
                    # ESPAÇO DISPONÍVEL
                    pdf.set_xy(x, y + (altura_card / 2) - 5)
                    pdf.set_font("Times", 'I', 10)
                    pdf.set_text_color(180, 180, 180)
                    pdf.cell(largura_card, 10, "ESPAÇO DISPONÍVEL", align='C')
                    pdf.set_text_color(0)

        pdf.output("jornal_talentos.pdf")
        print("✅ PDF gerado com fotos redondas e estrutura de 159 linhas preservada.")