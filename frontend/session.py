import streamlit as st


def init_auth_session() -> None:
    st.session_state.setdefault("is_authenticated", False)
    st.session_state.setdefault("access_token", None)
    st.session_state.setdefault("refresh_token", None)


def clear_auth_session() -> None:
    st.session_state["is_authenticated"] = False
    st.session_state["access_token"] = None
    st.session_state["refresh_token"] = None
