import streamlit as st
import pandas as pd
from datetime import datetime
from analyzer import calculate_totals, generate_savings_tip
from visualizer import plot_expense_bar, plot_saldo, plot_pie_chart
from predictor import predict_zero_balance
from pdf_report import generate_pdf

# 📐 Layout og stil
st.set_page_config(page_title="StudentBudsjett", page_icon="📊", layout="wide")

# 🎨 Profesjonell bakgrunn via CSS
st.markdown("""
    <style>
        body {
            background-color: #f4f6f8;
        }
        .stApp {
            background-color: #f4f6f8;
        }
        .css-1v3fvcr {
            background-color: #f4f6f8;
        }
    </style>
""", unsafe_allow_html=True)

# 🔧 Beregn saldo dynamisk
def beregn_saldo(df):
    saldo = 0
    saldo_liste = []
    for _, row in df.iterrows():
        if row["Type"] == "Inntekt":
            saldo += row["Beløp"]
        elif row["Type"] == "Utgift":
            saldo -= row["Beløp"]
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

# 📋 Sidebar: Transaksjoner og input
with st.sidebar:
    st.image("studentbudsjett_logo.png", width=150)
    st.title("📋 Kontrollpanel")

    st.subheader("🔍 Filtrer etter kategori")
    valgt_kategori = st.selectbox("Velg kategori", ["Alle"] + sorted(df["Kategori"].unique()))
    if valgt_kategori != "Alle":
        df = df[df["Kategori"] == valgt_kategori]

    st.subheader("➕ Legg til transaksjon")
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

    st.subheader("📄 Dine transaksjoner")
    st.dataframe(df, use_container_width=True)

# 📊 Hovedområde: Analyse og visualisering
st.title("📊 StudentBudsjett Analyse")

st.subheader("📈 Budsjettanalyse")
total_inntekt, total_utgift = calculate_totals(df)
st.write(f"Totale inntekter: {total_inntekt:.2f} kr")
st.write(f"Totale utgifter: {total_utgift:.2f} kr")

tips, level = generate_savings_tip(total_inntekt, total_utgift)
getattr(st, level)(tips)

if not df.empty:
    st.subheader("📊 Grafer")
    plot_expense_bar(df)
    plot_pie_chart(df[df["Type"] == "Utgift"].groupby("Kategori")["Beløp"].sum())
    plot_saldo(df)

    st.subheader("🔮 Prediksjon av fremtidig saldo")
    dato_null, trend = predict_zero_balance(df)
    if dato_null:
        st.warning(f"Basert på trenden vil saldoen nå 0 kr rundt {dato_null}.")
    else:
        st.success("Saldoen ser ut til å holde seg stabil eller øke.")

    st.subheader("📄 Last ned PDF-rapport")
    if st.button("Generer PDF"):
        df["Uke"] = df["Dato"].dt.isocalendar().week
        ukesaldo = df.groupby("Uke")["Saldo"].last()
        ukekategorier = df[df["Type"] == "Utgift"].groupby(["Uke", "Kategori"])["Beløp"].sum().unstack(fill_value=0)
        prediksjonstekst = f"Saldoen vil nå 0 kr rundt {dato_null}" if dato_null else "Saldoen ser stabil ut."
        pdf = generate_pdf(df, df["Saldo"].iloc[-1], prediksjonstekst, ukesaldo, ukekategorier)
        st.download_button("📥 Last ned PDF", data=pdf.output(dest="S").encode("latin-1"), file_name="studentbudsjett_rapport.pdf")
