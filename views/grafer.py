import streamlit as st
import pandas as pd
import altair as alt

from visualizer import plot_expense_bar, plot_pie_chart, plot_saldo

def vis(df):
    st.markdown("## 📈 Grafer")

    df["Uke"] = df["Dato"].dt.isocalendar().week
    kategorier = df["Kategori"].unique().tolist()
    valgte_kategorier = st.multiselect("Velg kategorier", kategorier, default=kategorier)

    valgte_uker = st.slider("Velg ukeintervall", int(df["Uke"].min()), int(df["Uke"].max()), (int(df["Uke"].min()), int(df["Uke"].max())))

    filtrert_df = df[
        (df["Kategori"].isin(valgte_kategorier)) &
        (df["Uke"] >= valgte_uker[0]) &
        (df["Uke"] <= valgte_uker[1])
    ]

    if filtrert_df.empty:
        st.warning("Ingen transaksjoner i valgt filter.")
        return

    # 📊 Utgifter per kategori per uke – stablet søylediagram
    utgifter = filtrert_df[filtrert_df["Type"] == "Utgift"]
    kategorier_per_uke = utgifter.groupby(["Uke", "Kategori"])["Beløp"].sum().reset_index()

    st.markdown("### 🧾 Utgifter per kategori per uke")
    søyler = alt.Chart(kategorier_per_uke).mark_bar().encode(
        x="Uke:O",
        y="Beløp:Q",
        color="Kategori:N",
        tooltip=["Uke", "Kategori", "Beløp"]
    ).properties(height=300)
    st.altair_chart(søyler, use_container_width=True)

    # 📈 Saldo over tid – linjediagram
    st.markdown("### 💰 Saldo over tid")
    saldo_per_dag = filtrert_df.groupby("Dato")["Saldo"].last().reset_index()
    linje = alt.Chart(saldo_per_dag).mark_line(point=True).encode(
        x="Dato:T",
        y="Saldo:Q",
        tooltip=["Dato", "Saldo"]
    ).properties(height=300)
    st.altair_chart(linje, use_container_width=True)
