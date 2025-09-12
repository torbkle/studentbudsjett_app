import streamlit as st

def vis_tom_df_melding(tittel="Ingen data tilgjengelig", beskrivelse="Legg til transaksjoner for å komme i gang."):
    st.markdown(f"### 📭 {tittel}")
    st.info(beskrivelse)
