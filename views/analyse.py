import streamlit as st
from analyzer import calculate_totals, generate_savings_tip

def vis(df):
    st.markdown("## 📊 Budsjettanalyse")
    inntekt, utgift = calculate_totals(df)
    col1, col2 = st.columns(2)
    col1.metric("Totale inntekter", f"{inntekt:.2f} kr")
    col2.metric("Totale utgifter", f"{utgift:.2f} kr")
    tips, level = generate_savings_tip(inntekt, utgift)
    getattr(st, level)(tips)
