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

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: #f5f5f7;
        color: #1d1d1f;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
    }
    .app-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 18px;
        padding: 24px;
        margin-top: 24px;
    }
    h1, h2, h3 {
        color: #1d1d1f;
        letter-spacing: -0.02em;
        font-weight: 600;
    }
    .stButton > button {
        background: #0066cc;
        color: #ffffff;
        border: 1px solid #0066cc;
        border-radius: 9999px;
        padding: 8px 22px;
    }
    .stButton > button:hover {
        background: #0071e3;
        border-color: #0071e3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_auth_session()

if not BACKEND_URL:
    st.error("La variable BACKEND_URL debe ser una URL válida (http/https).")
    st.stop()

st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.title("Iniciar sesión")
st.caption("Usa tus credenciales para acceder a la página de bienvenida.")

if st.session_state["is_authenticated"]:
    st.success("Ya tienes una sesión activa.")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Ir a bienvenida"):
            st.switch_page("pages/1_Bienvenida.py")
    with col_b:
        if st.button("Cerrar sesión"):
            clear_auth_session()
            st.rerun()
else:
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar")

    if submit:
        try:
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
                st.success("Login exitoso")
                st.switch_page("pages/1_Bienvenida.py")
            elif response.status_code == 401:
                st.error("Credenciales inválidas")
            else:
                st.error(f"Error inesperado del backend: {response.status_code}")
        except requests.RequestException as error:
            st.error(f"No fue posible conectar con el backend: {error}")

st.markdown("</div>", unsafe_allow_html=True)
