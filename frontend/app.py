import os
from urllib.parse import urlparse

import requests
import streamlit as st
from session import clear_auth_session, init_auth_session


def get_valid_backend_url() -> str | None:
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
    parsed_backend_url = urlparse(backend_url)
    if parsed_backend_url.scheme in {"http", "https"} and parsed_backend_url.netloc:
        return backend_url
    return None


BACKEND_URL = get_valid_backend_url()

st.set_page_config(page_title="Login", page_icon="🔐", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .login-container {
        background: transparent;
        backdrop-filter: none;
        border-radius: 24px;
        padding: 48px;
        box-shadow: none;
        max-width: 450px;
        margin: 0 auto;
    }
    .header-section {
        text-align: center;
        margin-bottom: 36px;
    }
    .logo-icon {
        font-size: 64px;
        margin-bottom: 16px;
    }
    h1 {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
        margin: 0 0 8px 0;
        letter-spacing: -1px;
    }
    .subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 14px;
        font-weight: 400;
    }
    .stTextInput > div {
        background: transparent !important;
    }
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        color: #ffffff !important;
        border-radius: 12px;
        transition: all 0.3s ease;
        padding: 10px 16px !important;
    }
    .stTextInput > div > div > input:focus {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    .stTextInput > label {
        color: #ffffff !important;
        font-weight: 500;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.6);
    }
    .success-section {
        text-align: center;
    }
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_auth_session()

if not BACKEND_URL:
    st.error("La variable BACKEND_URL debe ser una URL válida (http/https).")
    st.stop()

col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    if st.session_state["is_authenticated"]:
        st.markdown('<div class="success-section">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 48px; margin-bottom: 16px;">✅</div>', unsafe_allow_html=True)
        st.markdown('<h1>¡Sesión Activa!</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Tienes acceso a la plataforma</p>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Ir a Bienvenida", use_container_width=True):
                st.switch_page("pages/1_Bienvenida.py")
        with col_b:
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                clear_auth_session()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="header-section">', unsafe_allow_html=True)
        st.markdown('<div class="logo-icon">🔐</div>', unsafe_allow_html=True)
        st.markdown('<h1>Bienvenido</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Inicia sesión para continuar</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input("🔑 Contraseña", type="password", placeholder="Ingresa tu contraseña")
            st.markdown("")
            submit = st.form_submit_button("Ingresar", use_container_width=True)

        if submit:
            try:
                with st.spinner("Verificando credenciales..."):
                    response = requests.post(
                        f"{BACKEND_URL}/login",
                        json={"username": username, "password": password},
                        timeout=10,
                    )
                if response.status_code == 200:
                    payload = response.json()
                    st.session_state["is_authenticated"] = True
                    st.session_state["access_token"] = payload.get("access_token")
                    st.session_state["refresh_token"] = payload.get("refresh_token")
                    st.success("✅ Login exitoso. Redirigiendo...")
                    st.switch_page("pages/1_Bienvenida.py")
                elif response.status_code == 401:
                    st.error("❌ Credenciales inválidas. Intenta de nuevo.")
                else:
                    st.error(f"⚠️ Error del servidor: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar al backend. Verifica que esté en ejecución.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
