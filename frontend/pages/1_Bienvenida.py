import streamlit as st
from session import clear_auth_session, init_auth_session

st.set_page_config(page_title="Bienvenida", page_icon="👋", layout="centered")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: #272729;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
    }
    .app-card {
        background: #2a2a2c;
        border-radius: 18px;
        padding: 24px;
        margin-top: 24px;
        border: 1px solid rgba(224, 224, 224, 0.2);
    }
    h1, h2, h3, p {
        color: #ffffff;
        letter-spacing: -0.02em;
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

if not st.session_state.get("is_authenticated"):
    st.warning("Debes iniciar sesión para acceder a esta página")
    if st.button("Ir al login"):
        st.switch_page("app.py")
    st.stop()

st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.title("Bienvenido")
st.write("Tu sesión está activa y el acceso está protegido.")

if st.session_state.get("access_token"):
    st.caption("Token de acceso activo en sesión")

if st.button("Cerrar sesión"):
    clear_auth_session()
    st.switch_page("app.py")

st.markdown("</div>", unsafe_allow_html=True)
