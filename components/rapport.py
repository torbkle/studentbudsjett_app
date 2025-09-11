import streamlit as st
import pandas as pd
import altair as alt


def vis_rapportoppsummering(df):
    st.markdown("### 🧾 Rapportoppsummering")

    antall_transaksjoner = len(df)
    antall_uker = df["Dato"].dt.isocalendar().week.nunique()
    st.write(f"**Antall transaksjoner:** {antall_transaksjoner}")
    st.write(f"**Antall uker dekket:** {antall_uker}")

    df["Uke"] = df["Dato"].dt.isocalendar().week
    saldo_per_uke = df.groupby("Uke")["Saldo"].last().reset_index()
    utgifter = df[df["Type"] == "Utgift"]
    kategorier_per_uke = utgifter.groupby(["Uke", "Kategori"])["Beløp"].sum().reset_index()

    # 📊 Ukentlig saldo – linjediagram
    st.markdown("#### 📈 Ukentlig saldo")
    linje = alt.Chart(saldo_per_uke).mark_line(point=True).encode(
        x="Uke:O",
        y="Saldo:Q"
    ).properties(height=300)
    st.altair_chart(linje, use_container_width=True)

    # 📊 Utgifter per kategori – stablet søylediagram
    st.markdown("#### 📊 Utgifter per kategori per uke")
    søyler = alt.Chart(kategorier_per_uke).mark_bar().encode(
        x="Uke:O",
        y="Beløp:Q",
        color="Kategori:N",
        tooltip=["Uke", "Kategori", "Beløp"]
    ).properties(height=300)
    st.altair_chart(søyler, use_container_width=True)
