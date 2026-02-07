def get_custom_css(logo_html):
    """
    Retorna o CSS global e o HTML do cabeçalho estilo SaaS Moderno (Inhire).
    """
    return f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* 1. Configurações Globais */
        html, body {{
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }}
        
        .stMainBlockContainer.block-container{{
            padding: 0 !important;
        }}

        .stApp {{
            background-color: #f8fafc;
            color: #1e293b;
        }}

        /* 2. Cabeçalho Minimalista */
        .custom-header {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2.5rem 0;
            background: #ffffff;
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 3rem;
            font-size: 4rem;
        }}

        .logo-box {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .logo-img {{ width: 124px; object-fit: contain; }}
        
        .header-text {{ line-height: 1; }}
        .title-main {{ 
            font-size: 1.8rem; 
            font-weight: 800; 
            color: #0f172a; 
            margin: 0; 
            letter-spacing: -1px;
        }}
        .title-main span {{ color: #2563eb; }}
        
        .typing-text {{
            color: #64748b; 
            font-size: 0.8rem; 
            font-weight: 600; 
            text-transform: uppercase;
            letter-spacing: 0.2em; 
            margin-top: 5px;
        }}

        /* 3. Card do Formulário */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 30px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }}

        /* 4. Inputs Estilizados */
        div[data-baseweb="input"] {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }}

        div[data-baseweb="input"]:focus-within {{
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }}

        input {{ color: #1e293b !important; font-size: 1rem !important; }}
        
        label p {{
            color: #475569 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            text-transform: none !important;
        }}

        /* 5. Botão LinkedIn (Cor Oficial) */
        .stLinkButton > a, .stButton>button {{
            background-color: #0077b5 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1rem !important;
            font-weight: 600 !important;
            text-transform: none !important;
            letter-spacing: 0 !important;
            transition: all 0.2s ease !important;
        }}
        
        .stLinkButton > a:hover, .stButton>button:hover {{
            background-color: #005a87 !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }}

        /* Esconder decorações padrão */
        #MainMenu, footer, header {{visibility: hidden;}}
        
        .disclaimer-box {{
            margin-top: 25px;
            padding: 15px;
            border-radius: 8px;
            background: #f1f5f9;
        }}
        .disclaimer-text {{ color: #64748b; font-size: 0.8rem; text-align: center; }}
        </style>

        <div class="custom-header">
            <div class="logo-box">
                <img src="{logo_html}" class="logo-img">
                <div class="header-text">
                    <p class="title-main">TALENTOS <span>DIÁRIOS</span></p>
                    <div class="typing-text">Sua vitrine profissional</div>
                </div>
            </div>
        </div>
    """

def get_footer_html():
    return """
        <div style="text-align: center; padding: 20px; color: #94a3b8; font-size: 0.8rem; font-weight: 500;">
            Talentos Diários • 2026
        </div>
    """