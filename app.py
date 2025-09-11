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

setup()
init_db()

from db_handler import insert_transaksjon

# 🔁 Midlertidig testdata (kjør én gang)
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


df = hent_data()
df = beregn_saldo(df)
valg = sidebar()

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
