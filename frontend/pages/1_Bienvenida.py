import streamlit as st
from session import clear_auth_session, init_auth_session

st.set_page_config(page_title="Bienvenida", page_icon="👋", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        min-height: 100vh;
    }
    .welcome-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 48px 32px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 32px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
    }
    .welcome-header h1 {
        color: #ffffff;
        font-size: 48px;
        font-weight: 700;
        margin: 16px 0 8px 0;
        letter-spacing: -1px;
    }
    .welcome-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 18px;
        margin: 8px 0 0 0;
    }
    .emoji-lg {
        font-size: 64px;
        margin-bottom: 16px;
    }
    .info-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .info-card:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
    }
    .info-card h3 {
        color: #667eea;
        font-size: 18px;
        font-weight: 600;
        margin: 0 0 8px 0;
    }
    .info-card p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 14px;
        margin: 0;
    }
    .token-display {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
        padding: 16px;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.9);
        font-family: monospace;
        font-size: 12px;
        word-break: break-all;
        margin-bottom: 16px;
    }
    .logout-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .nav-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton > button {
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_auth_session()

if not st.session_state.get("is_authenticated"):
    st.markdown('<div style="text-align: center; margin-top: 100px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 64px; margin-bottom: 16px;">🔒</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="color: #ffffff;">Acceso Denegado</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255, 255, 255, 0.7);">Debes iniciar sesión para acceder</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Ir al Login", use_container_width=True):
            st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Welcome Header
st.markdown('<div class="welcome-header">', unsafe_allow_html=True)
st.markdown('<div class="emoji-lg">👋</div>', unsafe_allow_html=True)
st.markdown('<h1>¡Bienvenido a la Plataforma!</h1>', unsafe_allow_html=True)
st.markdown('<p>Tu sesión está activa y segura</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown('<h3>🔑 Estado de la Sesión</h3>', unsafe_allow_html=True)
    st.markdown('<p>Tu sesión está protegida con autenticación JWT</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.get("access_token"):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<h3>📋 Token de Acceso</h3>', unsafe_allow_html=True)
        with st.expander("Ver token"):
            st.markdown('<div class="token-display">' + st.session_state.get("access_token")[:50] + '...' + '</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown('<h3>✅ Características</h3>', unsafe_allow_html=True)
    st.markdown('<p>• Autenticación segura con JWT<br>• Tokens de acceso y refresco<br>• Sesión persistente<br>• Logout seguro</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_action1, col_action2 = st.columns(2)
    with col_action1:
        if st.button("🏠 Inicio", use_container_width=True):
            st.switch_page("app.py")
    with col_action2:
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            clear_auth_session()
            st.switch_page("app.py")
