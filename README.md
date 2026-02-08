# 🚀 Talentos Diários - Registrar

<img width="1917" height="965" alt="image" src="https://github.com/user-attachments/assets/fd857c4c-cde9-4ddb-ae6d-44a655bbcb76" />


Uma plataforma automatizada para conectar profissionais #OpenToWork a recrutadores, com geração notificações em tempo real.

## 🛠️ Tecnologias Utilizadas

O ecossistema do projeto é dividido entre a interface do usuário e o orquestrador de tarefas:

- **Interface Web:** [Streamlit](https://streamlit.io/)
- **Autenticação:** LinkedIn OAuth2 (OpenID Connect)
- **Geração de PDF:** [fpdf2](https://github.com/fpdf2/fpdf2) & [Pillow](https://python-pillow.org/)
- **Automação (CI/CD):** GitHub Actions
- **Comunicação:** OneSignal (Push Notifications) & FeedGen (RSS)
- **Gerenciamento de Dados:** [PyGithub](https://github.com/PyGithub/PyGithub) (Persistência no repositório)
- **Onesginal:** Notificação para inscritos
- **RSS:** Geração XML para notificação via RSS

## 🏗️ Arquitetura do Sistema

A aplicação funciona em um ciclo de automação contínua:

1. **Captação:** Candidatos se registram via Portal Streamlit usando a conta do LinkedIn.
2. **Persistência:** Os dados são validados e salvos em um repositório GitHub via API.
3. **Gatilho (Workflow):** A alteração nos dados dispara um GitHub Action.
4. **Processamento:** - O script Python lê o JSON de candidatos.
   - Gera um PDF otimizado com fotos (processamento de imagens em Base64).
   - Atualiza o Feed RSS.
5. **Notificação:** O OneSignal envia alertas sobre os novos talentos disponíveis.

Obs: O registro dura 30 dias em seguida é descartado.

## Exemplo: Json salvo

```
[
    {
        "nome": "Phillipe R.",
        "cargo": "C# | Fullstack Developer | .NET | Angular | Cloud & IA | Analista de Sistemas",
        "perfil_url": "https://www.linkedin.com/in/phillrog",
        "data_cadastro": "2026-02-05T07:52:35.168190",
        "foto": "data:image/jpeg;base64,...",
        "ativo": true
    }
]
```

⚠️ Disclaimer Este projeto é uma iniciativa de estudo e portfólio. O cadastro e a exibição na vitrine visam complementar sua visibilidade, não garantindo contratações ou propostas.

## 🔐 Autenticação e Privacidade

A segurança e a privacidade dos dados dos candidatos são prioridades neste projeto. Utilizamos o protocolo **OAuth 2.0** com o fluxo **OpenID Connect** para garantir uma integração segura com o LinkedIn.

### Escopos Utilizados (Scopes)
Solicitamos apenas as permissões mínimas necessárias para o funcionamento do serviço:
- `openid`: Identificação do usuário.
- `profile`: Acesso ao nome e foto de perfil utilizar no portal e no PDF.
- `email`: Utilizado apenas para o linkedin fazer o redirecionamento de volta para página.

<img width="479" height="782" alt="Captura de tela 2026-02-05 054101" src="https://github.com/user-attachments/assets/a7a89f08-5cc5-4df3-beb3-0aa02200a34b" />


## IMPORTANTE: 
Nenhum dado além deste é salvo ou lido. 

## 🏛️ Arquitetura e Boas Práticas

O projeto foi desenvolvido seguindo padrões de engenharia de software para garantir testabilidade e baixo acoplamento:
 
- **Clean Architecture**
- **SOLID**


## 🚀 Como Executar Localmente

### Requisitos
Precisa de um token github para escrever o json, gerar um token de acesso no linkedin para usar a api de autth e de um token Onesignal para notificações. Configurar as variáveis:

```
LINKEDIN_CLIENT_ID = ""
LINKEDIN_CLIENT_SECRET = ""
REDIRECT_URI = ""
LINKEDIN_ORG_ID = ""
LINKEDIN_PAGE_ACCESS_TOKEN =""
GITHUB_TOKEN=""
```



Siga os passos abaixo para configurar o ambiente e executar a aplicação localmente:

### 1. Criar o Ambiente Virtual
Isso garante que as bibliotecas do projeto não conflitem com outras no seu computador.
```bash
python -m venv .venv
```

### 2. Ativar o Ambiente Virtual

No Windows:

```bash
.\.venv\Scripts\activate
```

No Linux/Mac:

```bash
source .venv/bin/activate
```

### 3. Instalar as Dependências
Instale todas as bibliotecas necessárias listadas no arquivo requirements.txt.

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação
Inicie o servidor do Streamlit para abrir a interface no seu navegador.

```bash
python -m streamlit run app.py
```

Obs: Onesignal só funciona com https.

* * * * *

# Resultado

<img width="1917" height="965" alt="image" src="https://github.com/user-attachments/assets/fd857c4c-cde9-4ddb-ae6d-44a655bbcb76" />

<img width="1308" height="643" alt="image" src="https://github.com/user-attachments/assets/7106547f-d2c4-4213-8505-6736cd40a7d1" />

<img width="1312" height="645" alt="image" src="https://github.com/user-attachments/assets/af773010-d681-4dd0-91fe-88a9739e3471" />


Quem tiver se inscrito no [portal](https://talentos-diarios-portal.vercel.app/)  receberá esta mensagem

<img width="430" height="411" alt="image" src="https://github.com/user-attachments/assets/ef7e9764-9000-4d9c-aed9-83baeb52f0a6" />


