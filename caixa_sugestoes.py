"""
Playerz - Caixa de Sugestões
Canal de comunicação para dúvidas, sugestões e feedback dos usuários.
Envia notificações via Pushover para o desenvolvedor.
"""

import streamlit as st
import requests
from datetime import datetime

# =============================================================================
# CONFIGURAÇÃO DO PUSHOVER
# =============================================================================

try:
    PUSHOVER_USER_KEY = st.secrets.get("PUSHOVER_USER_KEY", "")
    PUSHOVER_API_TOKEN = st.secrets.get("PUSHOVER_API_TOKEN", "")
except Exception:
    PUSHOVER_USER_KEY = ""
    PUSHOVER_API_TOKEN = ""


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def send_contact_to_admin(user_name: str, user_email: str, category: str,
                          message: str, section: str = "Geral") -> bool:
    """Envia mensagem para o desenvolvedor via Pushover."""
    if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
        return False

    try:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

        pushover_message = f"""⚽ Nova mensagem - Playerz

📅 Data: {timestamp}
👤 Nome: {user_name}
📧 E-mail: {user_email if user_email else 'Não informado'}
📂 Categoria: {category}
📌 Seção: {section}

💬 Mensagem:
{message}"""

        priority = 0
        if category == "🚨 Erro/Bug no aplicativo":
            priority = 1

        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_API_TOKEN,
                "user": PUSHOVER_USER_KEY,
                "message": pushover_message,
                "title": f"Playerz - {category}",
                "priority": priority,
                "sound": "pushover"
            },
            timeout=10
        )

        return response.status_code == 200

    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout ao enviar mensagem. Tente novamente.")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        st.error(f"❌ Erro ao enviar notificação: {e}")
        return False


def validate_email(email: str) -> bool:
    """Validação simples de formato de e-mail."""
    if not email:
        return False
    if "@" not in email or "." not in email:
        return False
    if len(email) < 5:
        return False
    return True


def validate_message(message: str, min_length: int = 10) -> bool:
    """Valida se a mensagem tem conteúdo mínimo."""
    if not message:
        return False
    if len(message.strip()) < min_length:
        return False
    return True


# =============================================================================
# FUNÇÃO PRINCIPAL DE RENDERIZAÇÃO
# =============================================================================

def render():
    """Função principal que renderiza o módulo completo."""

    # Introdução
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### Fale com o Desenvolvedor

        Use este canal para:
        - 🤔 **Tirar dúvidas** sobre funcionalidades do app
        - 💡 **Enviar sugestões** de novas features ou melhorias
        - 🐛 **Reportar erros** ou problemas técnicos
        - 📊 **Sugerir métricas** ou análises de jogadores
        - 💬 **Fazer comentários** gerais sobre o Playerz
        """)

    with col2:
        st.info("""
        💡 **Dica**

        Seja específico na sua mensagem!

        Inclua a seção do app e
        detalhes relevantes para
        facilitar o atendimento.
        """)

    st.markdown("---")

    # Verificar configuração do Pushover
    pushover_configured = bool(PUSHOVER_USER_KEY and PUSHOVER_API_TOKEN)

    if not pushover_configured:
        st.warning("""
        ⚠️ **Sistema de notificação não configurado**

        O envio de mensagens está temporariamente indisponível.
        """)

    # Formulário
    st.subheader("📝 Envie sua Mensagem")

    with st.form(key="contact_form", clear_on_submit=True):

        # Dados do usuário
        col1, col2 = st.columns(2)

        with col1:
            user_name = st.text_input(
                "👤 Seu nome *",
                placeholder="Digite seu nome",
                max_chars=100
            )

        with col2:
            user_email = st.text_input(
                "📧 Seu e-mail (opcional)",
                placeholder="seu.email@exemplo.com",
                max_chars=100
            )

        # Categoria e seção
        col1, col2 = st.columns(2)

        with col1:
            category = st.selectbox(
                "📂 Categoria *",
                options=[
                    "🤔 Dúvida sobre funcionalidade",
                    "💡 Sugestão de melhoria",
                    "🚨 Erro/Bug no aplicativo",
                    "📊 Sugestão de métrica/análise",
                    "📝 Feedback geral",
                    "💬 Outro assunto"
                ]
            )

        with col2:
            section = st.selectbox(
                "📌 Seção relacionada",
                options=[
                    "Geral / Não se aplica",
                    "Perfil do Jogador",
                    "Comparação de Jogadores",
                    "Rankings e Classificações",
                    "Análise de Desempenho",
                    "Scouting / Radar",
                    "Dados e Estatísticas",
                    "Visualizações e Gráficos",
                    "Interface / Navegação"
                ]
            )

        # Mensagem
        message = st.text_area(
            "💬 Sua mensagem *",
            placeholder="Descreva sua dúvida, sugestão ou feedback em detalhes...\n\n"
                        "Se for um erro, inclua:\n"
                        "- O que você estava fazendo\n"
                        "- O que aconteceu\n"
                        "- O que era esperado",
            height=200,
            max_chars=2000
        )

        # Contador de caracteres
        char_count = len(message) if message else 0
        st.caption(f"{char_count}/2000 caracteres")

        # Botão de envio
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            submitted = st.form_submit_button(
                "📤 Enviar Mensagem",
                use_container_width=True,
                type="primary"
            )

    # Processamento do envio
    if submitted:
        errors = []

        if not user_name or len(user_name.strip()) < 2:
            errors.append("Por favor, informe seu nome.")

        if user_email and not validate_email(user_email):
            errors.append("O e-mail informado não parece válido.")

        if not validate_message(message, min_length=10):
            errors.append("A mensagem deve ter pelo menos 10 caracteres.")

        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            if not pushover_configured:
                st.error("❌ Sistema de envio não configurado. Tente novamente mais tarde.")
            else:
                with st.spinner("📤 Enviando mensagem..."):
                    success = send_contact_to_admin(
                        user_name=user_name.strip(),
                        user_email=user_email.strip(),
                        category=category,
                        message=message.strip(),
                        section=section
                    )

                if success:
                    reply_msg = "Aguarde o retorno pelo e-mail informado." if user_email.strip() else ""
                    st.success(f"""
                    ✅ **Mensagem enviada com sucesso!**

                    O desenvolvedor receberá sua mensagem em instantes.
                    {reply_msg}

                    Obrigado pelo seu feedback! ⚽
                    """)
                    st.balloons()
                else:
                    st.error("""
                    ❌ **Erro ao enviar mensagem**

                    Ocorreu um problema no envio. Por favor, tente novamente.
                    """)

    st.markdown("---")

    # FAQ
    st.subheader("❓ Perguntas Frequentes")

    with st.expander("Quanto tempo para receber uma resposta?"):
        st.markdown("""
        O desenvolvedor receberá sua mensagem imediatamente via notificação.
        O tempo de resposta varia, mas geralmente:

        - **Dúvidas simples:** 24-48 horas
        - **Sugestões:** Avaliadas semanalmente
        - **Erros/Bugs:** Priorizados para correção rápida
        """)

    with st.expander("Posso enviar anexos ou imagens?"):
        st.markdown("""
        No momento, este formulário aceita apenas texto.

        Se precisar enviar capturas de tela, mencione isso na mensagem
        e o desenvolvedor entrará em contato por e-mail para solicitar
        os materiais adicionais.
        """)

    with st.expander("Encontrei um erro nos dados de um jogador"):
        st.markdown("""
        Ao reportar erros nos dados, informe:

        - **Nome do jogador** e temporada
        - **Qual dado está errado** (gols, assistências, etc.)
        - **Qual deveria ser o valor correto** (se souber)
        - **Fonte de referência** (se tiver)
        """)

    with st.expander("Quero sugerir uma nova funcionalidade"):
        st.markdown("""
        Adoramos receber sugestões! Para facilitar a avaliação:

        - **Descreva a funcionalidade** desejada
        - **Explique o contexto** de uso
        - **Dê exemplos** de como seria útil
        """)