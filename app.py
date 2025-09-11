import streamlit as st
import pandas as pd
from datetime import datetime
from db_handler import init_db, hent_data
from layout import setup, sidebar
from views import oversikt, analyse, grafer, prediksjon, pdf_rapport, legg_til

def beregn_saldo(df):
    saldo = 0
    saldo_liste = []
    for _, row in df.iterrows():
        saldo += row["Beløp"] if row["Type"] == "Inntekt" else -row["Beløp"]
        saldo_liste.append(saldo)
    df["Saldo"] = saldo_liste
    return df
def legg_inn_testdata():
    from db_handler import insert_transaksjon
    testdata = [
        ("2025-09-01", "Inntekt", 12000, "Stipend"),
        ("2025-09-03", "Utgift", 450, "Mat"),
        ("2025-09-05", "Utgift", 1200, "Leie"),
        ("2025-09-07", "Utgift", 300, "Transport"),
        ("2025-09-10", "Inntekt", 2000, "Ekstrajobb"),
        ("2025-09-11", "Utgift", 150, "Kaffe"),
    ]
    for dato, type_, beløp, kategori in testdata:
        insert_transaksjon(dato, type_, beløp, kategori)

setup()
init_db()




df = hent_data()
df = beregn_saldo(df)
valg, utviklermodus = sidebar()

from db_handler import tøm_database

if utviklermodus:
    with st.sidebar.expander("🧪 Testverktøy", expanded=False):
        st.markdown("### 📦 Eksporter til CSV")

        filnavn = st.text_input("Filnavn (uten .csv):", value="studentbudsjett_backup", key="csv_filnavn")
        kun_filtrert = st.checkbox("Kun synlige transaksjoner", key="csv_filter_toggle")

        if st.button("Eksporter", key="eksporter_csv"):
            try:
                eksport_df = df if not kun_filtrert else df[df["Vis"] == True] if "Vis" in df.columns else df
                eksport_df.to_csv(f"{filnavn}.csv", index=False)
                st.success(f"Backup lagret som {filnavn}.csv")
            except Exception as e:
                st.error(f"Feil under eksport: {e}")


        if st.button("Fyll med testdata", key="fyll_testdata"):
            try:
                legg_inn_testdata()
                st.success("Testdata lagt inn!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Feil under innlegging: {e}")

        if st.button("Tøm databasen", key="tøm_db"):
            try:
                tøm_database()
                st.success("Databasen er tømt.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Feil under sletting: {e}")

        # 📦 Eksporter til CSV
        if st.button("Eksporter til CSV", key="eksporter_csv"):
            try:
                df.to_csv("studentbudsjett_backup.csv", index=False)
                st.success("Backup lagret som studentbudsjett_backup.csv")
            except Exception as e:
                st.error(f"Feil under eksport: {e}")


if valg == "📄 Oversikt":
    oversikt.vis(df)
elif valg == "📊 Analyse":
    analyse.vis(df)
elif valg == "📈 Grafer":
    grafer.vis(df)
elif valg == "🔮 Prediksjon":
    prediksjon.vis(df)
elif valg == "📥 PDF-rapport":
    pdf_rapport.vis(df)
elif valg == "➕ Legg til transaksjon":
    legg_til.vis()
