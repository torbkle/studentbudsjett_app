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
        
        # 🔧 Utviklerknapp (kun for deg)
        if st.checkbox("🧪 Fyll med testdata"):
            from app import legg_inn_testdata
            legg_inn_testdata()
            st.success("Testdata lagt inn!")
            st.experimental_rerun()

        return valg
