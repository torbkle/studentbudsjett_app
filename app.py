import streamlit as st
import pandas as pd
from datetime import datetime
from analyzer import calculate_totals, generate_savings_tip
from visualizer import plot_expense_bar, plot_saldo, plot_pie_chart
from predictor import predict_zero_balance
from pdf_report import generate_pdf

st.set_page_config(page_title="StudentBudsjett", page_icon="📊", layout="wide")

# 🔧 Beregn saldo
def beregn_saldo(df):
    saldo = 0
    saldo_liste = []
    for _, row in df.iterrows():
        saldo += row["Beløp"] if row["Type"] == "Inntekt" else -row["Beløp"]
        saldo_liste.append(saldo)
    df["Saldo"] = saldo_liste
    return df

# 📥 Last inn data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("studentbudsjett_data.csv", parse_dates=["Dato"])
        df.sort_values("Dato", inplace=True)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Dato", "Type", "Beløp", "Kategori"])

df = load_data()
df = beregn_saldo(df)

# 🧭 Navigasjonsmeny
with st.sidebar:
    st.image("studentbudsjett_logo.png", width=150)
    st.title("📋 Navigasjon")
    valg = st.radio("Gå til seksjon:", [
        "Oversikt", "Analyse", "Grafer", "Prediksjon", "PDF-rapport", "Legg til transaksjon"
    ])

# 📋 Seksjon: Oversikt
if valg == "Oversikt":
    st.header("📋 Dine transaksjoner")
    st.dataframe(df, use_container_width=True)

# 📊 Seksjon: Analyse
elif valg == "Analyse":
    st.header("📊 Budsjettanalyse")
    inntekt, utgift = calculate_totals(df)
    st.metric("Totale inntekter", f"{inntekt:.2f} kr")
    st.metric("Totale utgifter", f"{utgift:.2f} kr")
    tips, level = generate_savings_tip(inntekt, utgift)
    getattr(st, level)(tips)

# 📈 Seksjon: Grafer
elif valg == "Grafer":
    st.header("📈 Visualisering")
    plot_expense_bar(df)
    plot_pie_chart(df[df["Type"] == "Utgift"].groupby("Kategori")["Beløp"].sum())
    plot_saldo(df)

# 🔮 Seksjon: Prediksjon
elif valg == "Prediksjon":
    st.header("🔮 Prediksjon av saldo")
    dato_null, trend = predict_zero_balance(df)
    if dato_null:
        st.warning(f"Saldoen vil nå 0 kr rundt {dato_null}.")
    else:
        st.success("Saldoen ser ut til å holde seg stabil eller øke.")

# 📄 Seksjon: PDF-rapport
elif valg == "PDF-rapport":
    st.header("📄 Generer PDF-rapport")
    if st.button("Generer PDF"):
        df["Uke"] = df["Dato"].dt.isocalendar().week
        ukesaldo = df.groupby("Uke")["Saldo"].last()
        ukekategorier = df[df["Type"] == "Utgift"].groupby(["Uke", "Kategori"])["Beløp"].sum().unstack(fill_value=0)
        prediksjonstekst = f"Saldoen vil nå 0 kr rundt {dato_null}" if dato_null else "Saldoen ser stabil ut."
        pdf = generate_pdf(df, df["Saldo"].iloc[-1], prediksjonstekst, ukesaldo, ukekategorier)
        st.download_button("📥 Last ned PDF", data=pdf.output(dest="S").encode("latin-1"), file_name="studentbudsjett_rapport.pdf")

# ➕ Seksjon: Legg til transaksjon
elif valg == "Legg til transaksjon":
    st.header("➕ Legg til ny transaksjon")
    with st.form("ny_transaksjon"):
        dato = st.date_input("Dato", value=datetime.today())
        type_ = st.selectbox("Type", ["Inntekt", "Utgift"])
        beløp = st.number_input("Beløp", min_value=0.0, step=100.0)
        kategori = st.text_input("Kategori")
        submit = st.form_submit_button("Legg til")

        if submit and kategori:
            ny_rad = pd.DataFrame({
                "Dato": [pd.to_datetime(dato)],
                "Type": [type_],
                "Beløp": [beløp],
                "Kategori": [kategori]
            })
            df = pd.concat([df, ny_rad], ignore_index=True)
            df.sort_values("Dato", inplace=True)
            df = beregn_saldo(df)
            df.to_csv("studentbudsjett_data.csv", index=False)
            st.success("Transaksjon lagt til! Oppdater siden for å se endringen.")
