import streamlit as st
from predictor import predict_zero_balance

def vis(df):
    st.markdown("## 🔮 Prediksjon av saldo")
    dato_null, trend = predict_zero_balance(df)
    if dato_null:
        st.warning(f"Saldoen vil nå 0 kr rundt {dato_null}.")
    else:
        st.success("Saldoen ser ut til å holde seg stabil eller øke.")
