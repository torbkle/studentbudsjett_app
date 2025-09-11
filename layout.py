import streamlit as st

def setup():
    st.set_page_config(
        page_title="StudentBudsjett",
        page_icon="💸",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

def sidebar():
    st.sidebar.image("studentbudsjett_logo.png", use_container_width=True)
    st.sidebar.markdown("## Navigasjon")

    valg = st.sidebar.radio(
        "Velg visning:",
        [
            "📄 Oversikt",
            "📊 Analyse",
            "📈 Grafer",
            "🔮 Prediksjon",
            "📥 PDF-rapport",
            "➕ Legg til transaksjon"
        ]
    )

    utviklermodus = st.sidebar.checkbox("Utviklermodus", value=False)
    return valg, utviklermodus
