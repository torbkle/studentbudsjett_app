import streamlit as st
import pandas as pd

def vis_tabell(df, tittel="Transaksjoner", maks_rader=10):
    st.markdown(f"### 📋 {tittel}")
    if df.empty:
        st.info("Ingen data å vise.")
    else:
        st.dataframe(df.tail(maks_rader), use_container_width=True)
