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
