# app.py
import streamlit as st
import pandas as pd
import datetime


# Vis banner øverst
st.image("banner.png", use_column_width=True)

# Tittel og introduksjon
st.title("📊 StudentBudsjett App")
st.write("Hold oversikt over inntekter og utgifter – og få prediksjon på når du går tom for penger.")

# Vis logo under introduksjon
st.image("studentbudsjett_logo.png", width=200)

st.sidebar.header("Legg til transaksjon")
trans_type = st.sidebar.selectbox("Type", ["Inntekt", "Utgift"])
amount = st.sidebar.number_input("Beløp (kr)", min_value=0.0, step=10.0)
category = st.sidebar.selectbox("Kategori", ["Mat", "Bolig", "Transport", "Fritid", "Annet"])
date = st.sidebar.date_input("Dato", value=datetime.date.today())

if st.sidebar.button("Legg til"):
    new_data = {"Dato": date, "Type": trans_type, "Beløp": amount, "Kategori": category}
    st.session_state.setdefault("transaksjoner", []).append(new_data)
    st.success("Transaksjon lagt til!")

st.subheader("📋 Dine transaksjoner")
df = pd.DataFrame(st.session_state.get("transaksjoner", []))
if not df.empty:
    st.dataframe(df)
    saldo = df.apply(lambda row: row["Beløp"] if row["Type"] == "Inntekt" else -row["Beløp"], axis=1).sum()
    st.metric("💰 Nåværende saldo", f"{saldo:.2f} kr")
else:
    st.info("Ingen transaksjoner registrert ennå.")
