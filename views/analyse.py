import streamlit as st
import pandas as pd
import altair as alt

from analyzer import calculate_totals, generate_savings_tip
from components.infoboks import vis_infoboks
from components.tabell import vis_tabell


def vis(df):
    st.markdown("## 📊 Analyse")

    utgifter = df[df["Type"] == "Utgift"]
    total_utgift = utgifter["Beløp"].sum()
    antall_utgifter = len(utgifter)

    vis_infoboks("Totale utgifter", f"{total_utgift:.2f} kr", ikon="💸", farge="#B22222")
    vis_infoboks("Antall utgiftstransaksjoner", f"{antall_utgifter}", ikon="🧾", farge="#8B0000")

    # 📊 Sektordiagram – utgifter per kategori
    st.markdown("### 🧭 Fordeling per kategori")
    kategori_sum = utgifter.groupby("Kategori")["Beløp"].sum().reset_index()
    pie = alt.Chart(kategori_sum).mark_arc(innerRadius=50).encode(
        theta="Beløp:Q",
        color="Kategori:N",
        tooltip=["Kategori", "Beløp"]
    ).properties(height=300)
    st.altair_chart(pie, use_container_width=True)

    # 📈 Linjediagram – utgifter over tid
    st.markdown("### 📈 Utvikling over tid")
    daglig_sum = utgifter.groupby("Dato")["Beløp"].sum().reset_index()
    linje = alt.Chart(daglig_sum).mark_line(point=True).encode(
        x="Dato:T",
        y="Beløp:Q",
        tooltip=["Dato", "Beløp"]
    ).properties(height=300)
    st.altair_chart(linje, use_container_width=True)

    # 📋 Tabell med utgifter
    vis_tabell(utgifter, tittel="Utgiftstransaksjoner")
