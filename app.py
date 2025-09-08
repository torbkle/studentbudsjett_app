# app.py
import streamlit as st
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# 📌 Logo og introduksjon
st.image("studentbudsjett_logo.png", width=200)
st.write("Hold oversikt over inntekter og utgifter – og få prediksjon på når du går tom for penger.")

# 📋 Sidepanel for transaksjoner
st.sidebar.header("Legg til transaksjon")
trans_type = st.sidebar.selectbox("Type", ["Inntekt", "Utgift"])
amount = st.sidebar.number_input("Beløp (kr)", min_value=0.0, step=10.0)
category = st.sidebar.selectbox("Kategori", ["Mat", "Bolig", "Transport", "Fritid", "Annet"])
date = st.sidebar.date_input("Dato", value=datetime.date.today())

if st.sidebar.button("Legg til"):
    new_data = {"Dato": date, "Type": trans_type, "Beløp": amount, "Kategori": category}
    st.session_state.setdefault("transaksjoner", []).append(new_data)
    st.success("Transaksjon lagt til!")

# 📊 Vis transaksjoner og analyser
st.subheader("📋 Dine transaksjoner")
df = pd.DataFrame(st.session_state.get("transaksjoner", []))

if not df.empty:
    df["Dato"] = pd.to_datetime(df["Dato"])  # 🔧 Sikre riktig datoformat
    st.dataframe(df)

    # 💰 Beregn saldo
    saldo = df.apply(lambda row: row["Beløp"] if row["Type"] == "Inntekt" else -row["Beløp"], axis=1).sum()
    st.metric("💰 Nåværende saldo", f"{saldo:.2f} kr")

    # 🔮 Prediksjon: Når går du tom for penger?
    df["Beløp_signed"] = df.apply(lambda row: row["Beløp"] if row["Type"] == "Inntekt" else -row["Beløp"], axis=1)
    df_sorted = df.sort_values("Dato")
    df_sorted["Saldo"] = df_sorted["Beløp_signed"].cumsum()
    df_sorted["Dag"] = (df_sorted["Dato"] - df_sorted["Dato"].min()).dt.days

    X = df_sorted[["Dag"]]
    y = df_sorted["Saldo"]
    model = LinearRegression()
    model.fit(X, y)

    if model.coef_[0] < 0:
        dag_null = -model.intercept_ / model.coef_[0]
        dato_null = df_sorted["Dato"].min() + pd.Timedelta(days=dag_null)
        st.warning(f"🔮 Prediksjon: Du går tom for penger rundt {dato_null.date()}")
    else:
        st.success("🔮 Prediksjon: Saldoen din vokser – ingen fare for tom konto!")

    # 📈 Visualiser saldoen over tid
    fig1, ax1 = plt.subplots()
    ax1.plot(df_sorted["Dato"], df_sorted["Saldo"], marker="o", linestyle="-", color="teal")
    ax1.set_title("Saldo over tid")
    ax1.set_xlabel("Dato")
    ax1.set_ylabel("Saldo (kr)")
    ax1.grid(True)
    st.pyplot(fig1)

    # 🥧 Kakediagram over utgifter per kategori
    utgifter = df[df["Type"] == "Utgift"]
    if not utgifter.empty:
        kategori_sum = utgifter.groupby("Kategori")["Beløp"].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(kategori_sum, labels=kategori_sum.index, autopct="%1.1f%%", startangle=90)
        ax2.set_title("Fordeling av utgifter")
        st.subheader("📊 Fordeling av utgifter")
        st.pyplot(fig2)

else:
    st.info("Ingen transaksjoner registrert ennå.")
