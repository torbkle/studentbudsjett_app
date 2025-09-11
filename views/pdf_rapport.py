import streamlit as st

from pdf_report import generate_pdf

def vis(df):
    st.markdown("## 📥 Generer PDF-rapport")
    if st.button("Generer PDF"):
        df["Uke"] = df["Dato"].dt.isocalendar().week
        generate_pdf(df)
        st.success("PDF generert.")
