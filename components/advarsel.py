import streamlit as st

def vis_advarsel(melding, bekreft_nøkkel):
    st.warning(melding)
    return st.checkbox("Jeg bekrefter", key=bekreft_nøkkel)
