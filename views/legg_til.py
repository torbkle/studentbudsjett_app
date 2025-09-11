import streamlit as st
from datetime import datetime
from db_handler import insert_transaksjon

def vis():
    st.markdown("## ➕ Legg til ny transaksjon")
    with st.form("ny_transaksjon"):
        dato = st.date_input("Dato", value=datetime.today())
        type_ = st.selectbox("Type", ["Inntekt", "Utgift"])
        beløp = st.number_input("Beløp", min_value=0.0, step=10.0)
        kategori = st.text_input("Kategori")
        submit = st.form_submit_button("Legg til")

    if submit and kategori:
        insert_transaksjon(dato, type_, beløp, kategori)
        st.success("Transaksjon lagt til!")
        if st.button("🔄 Oppdater visning"):
            st.experimental_rerun()
