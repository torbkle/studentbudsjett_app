import streamlit as st
from pdf_report import lag_pdf_rapport

def vis(df):
    st.markdown("## 📥 PDF-rapport")
    try:
        lag_pdf_rapport(df)
        with open("rapport.pdf", "rb") as f:
            st.download_button("Last ned PDF", f, file_name="StudentBudsjett_Rapport.pdf")
        st.success("PDF generert!")
    except Exception as e:
        st.error(f"Feil under PDF-generering: {e}")
