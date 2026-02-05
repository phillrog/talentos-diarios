def get_custom_css(logo_html):
    """
    Retorna o CSS global e o HTML do cabeçalho personalizado.
    """
    return f"""
        <style>
        /* 1. Configurações Globais e Fontes */
        html, body, [class*="st-"] {{
            font-size: 1.05rem;
        }}

        .stApp, .stAppHeader {{
            background-color: #020617;
            color: #f8f9fa;
        }}

        /* 2. Cabeçalho Customizado (Glassmorphism) */
        .custom-header {{
            display: flex;
            align-items: center;
            padding: 2.5rem 10%;
            background: rgba(2, 6, 23, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 3.5rem;
        }}

        .logo-box {{
            background: linear-gradient(135deg, #1e293b 0%, #020617 100%);
            padding: 15px;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.35);
            display: flex;
            align-items: center;
            justify-content: center;
            scale: 1.5;
        }}

        .logo-img {{ width: 60px; height: 60px; object-fit: contain; }}
        
        .title-container {{ margin-left: 28px; line-height: 0.85; font-size: 3rem; }}
        
        .title-main {{ font-size: 3.5rem; font-weight: 900; color: white; margin: 0; letter-spacing: -2px; }}
        .title-sub {{ 
            font-size: 3.5rem; font-weight: 900; color: #3b82f6; margin: 0; letter-spacing: -2px; 
            filter: drop-shadow(0 0 15px rgba(59, 130, 246, 0.5)); 
        }}
        
        .typing-text {{
            color: #10b981; font-size: 15px; font-weight: 800; text-transform: uppercase;
            letter-spacing: 0.35em; margin-top: 15px; display: flex; align-items: center; gap: 10px;
        }}
        .typing-text::before {{ content: ""; width: 30px; height: 2px; background: #3b82f6; display: inline-block; }}

        /* 3. Estilização do Card do Formulário */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: #0e162b !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 24px !important;
            padding: 25px !important;
        }}

        /* 4. Estilização dos Inputs (Efeito Glow & Rounded) */
        div[data-baseweb="input"] {{
            background-color: rgba(15, 23, 42, 0.9) !important;
            border: 2px solid #1e293b !important;
            border-radius: 2rem !important;
            padding: 12px 24px !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        }}

        div[data-baseweb="input"]:focus-within {{
            border-color: #3b82f6 !important;
            box-shadow: 0 0 40px rgba(37, 99, 235, 0.15) !important;
            transform: translateY(-2px);
        }}

        input {{ 
            color: #46556a !important; 
            font-size: 1.4rem !important;
            font-weight: 500 !important;
        }}
        
        input::placeholder {{
            color: #334155 !important;
            font-size: 1.1rem;
        }}

        div[data-baseweb="input"] > div {{
            border: none !important;
            background-color: transparent !important;
        }}

        label p {{
            color: #46556a !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            margin-bottom: 12px !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* 5. Botão Primário Imponente */
        .stButton>button {{
            color: rgb(49, 51, 63) !important;
            background-color: #fff !important;
            border: none !important;
            padding: 1.2rem 2rem !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
            border-radius: 2rem !important;
            transition: all 0.3s ease !important;
            margin-top: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(37, 99, 235, 0.5) !important;
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
            color: #fff !important;
        }}

        /* 6. Ajustes de Layout e Main Container */
        div[data-testid="stLayoutWrapper"] div[data-testid="stLayoutWrapper"] {{
            background-color: #0e162b !important;
        }}
        
        div[data-testid="stMainBlockContainer"] {{
            padding: 1rem !important;
        }}

        /* Esconder decorações padrão do Streamlit */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
            
        .disclaimer-box {{
            margin-top: 25px;
            padding: 15px 20px;
            border-radius: 1rem;
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .disclaimer-text {{
            color: #46556a;
            font-size: 0.85rem;
            line-height: 1.5;
            margin: 0;
            text-align: center;
            font-weight: 500;
        }}
        
            
        .stLinkButton > a {{
            color: #fff !important; /* Texto branco como padrão já que terá gradiente */
            background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
            border: none !important;
            padding: 1.2rem 2rem !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
            border-radius: 2rem !important;
            transition: all 0.3s ease !important;
            margin-top: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
            display: flex; /* Garante que o conteúdo fique centralizado */
            justify-content: center;
            align-items: center;
            text-decoration: none !important; /* Remove sublinhado de link */
        }}

        /* Hover para o Botão de Link */
        .stLinkButton > a:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(37, 99, 235, 0.5) !important;
            filter: brightness(1.1); /* Dá um leve brilho no hover */
            color: #fff !important;
        }}

        .stLinkButton span {{
            color: #fff !important;
        }}
        </style>

        <div class="custom-header">
            <div class="logo-box">
                <img src="{logo_html}" class="logo-img">
            </div>
            <div class="title-container">
                <p class="title-main">TALENTOS</p>
                <p class="title-sub">DIÁRIOS</p>
                <div class="typing-text">Open To Work _</div>
            </div>
        </div>
        
    """

def get_footer_html():
    """
    Retorna o HTML do rodapé minimalista estilizado.
    """
    return """
        <style>
        .footer-container {
            width: 100%;
            text-align: center;
            margin-top: 20px;
        }
        .footer-text {
            color: #46556a;
            font-size: 10px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.5em;
            opacity: 0.8;
            transition: opacity 0.3s ease;
        }
        .footer-text:hover {
            opacity: 1;
            color: #3b82f6;
        }
        
        .vitrine-link-container {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
        }
        .vitrine-link {
            color: #3b82f6 !important;
            font-weight: 800;
            text-decoration: none;
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 0.1em;
            transition: all 0.3s ease;
        }
        .vitrine-link:hover {
            color: #10b981 !important;
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        }
        </style>
        
        <div class="footer-container">
            <p class="footer-text">Talentos Diários • 2026</p>
        </div>
    """