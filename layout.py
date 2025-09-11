import streamlit as st

def setup():
    st.set_page_config(page_title="StudentBudsjett", page_icon="📊", layout="wide")

def sidebar():
    with st.sidebar:
        st.image("studentbudsjett_logo.png", width=150)
        st.markdown("## 📋 Navigasjon")
        valg = st.radio("Velg seksjon:", [
            "📄 Oversikt", "📊 Analyse", "📈 Grafer", "🔮 Prediksjon", "📥 PDF-rapport", "➕ Legg til transaksjon"
        ])
        utviklermodus = st.checkbox("🛠️ Utviklermodus", key="utviklermodus_toggle")
        return valg, utviklermodus
