import streamlit as st
import pandas as pd

def vis_rapportoppsummering(df):
    st.markdown("### 🧾 Rapportoppsummering")

    antall_transaksjoner = len(df)
    antall_uker = df["Dato"].dt.isocalendar().week.nunique()
    st.write(f"**Antall transaksjoner:** {antall_transaksjoner}")
    st.write(f"**Antall uker dekket:** {antall_uker}")

    df["Uke"] = df["Dato"].dt.isocalendar().week
    saldo_per_uke = df.groupby("Uke")["Saldo"].last().reset_index()
    utgifter = df[df["Type"] == "Utgift"]
    kategorier_per_uke = utgifter.groupby(["Uke", "Kategori"])["Beløp"].sum().unstack(fill_value=0)

    st.markdown("#### 📅 Ukentlig saldo")
    st.dataframe(saldo_per_uke, use_container_width=True)

    st.markdown("#### 🧾 Utgifter per kategori per uke")
    st.dataframe(kategorier_per_uke, use_container_width=True)
