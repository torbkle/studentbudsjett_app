import streamlit as st
import pandas as pd
from datetime import datetime
from analyzer import calculate_totals, generate_savings_tip
from visualizer import plot_expense_bar, plot_saldo, plot_pie_chart
from predictor import predict_zero_balance
from pdf_report import generate_pdf
from db_handler import init_db, insert_transaksjon, hent_data
from db_handler import slett_transaksjon

init_db()

# 🔧 Beregn saldo
def beregn_saldo(df):
    saldo = 0
    saldo_liste = []
    for _, row in df.iterrows():
        saldo += row["Beløp"] if row["Type"] == "Inntekt" else -row["Beløp"]
        saldo_liste.append(saldo)
    df["Saldo"] = saldo_liste
    return df


df = hent_data()
df = beregn_saldo(df)


st.set_page_config(page_title="StudentBudsjett", page_icon="📊", layout="wide")



# 📥 Last inn data


# 🧭 Navigasjonsmeny med ikoner
with st.sidebar:
    st.image("studentbudsjett_logo.png", width=150)
    st.markdown("## 📋 Navigasjon")
    valg = st.radio("Velg seksjon:", [
        "📄 Oversikt",
        "📊 Analyse",
        "📈 Grafer",
        "🔮 Prediksjon",
        "📥 PDF-rapport",
        "➕ Legg til transaksjon"
    ])

# 📄 Oversikt
if valg == "📄 Oversikt":
    st.markdown("## 📄 Dine transaksjoner")

    # 🔍 Filtrering
    type_filter = st.selectbox("Filtrer etter type:", ["Alle", "Inntekt", "Utgift"])
    kategori_filter = st.text_input("Filtrer etter kategori (valgfritt):")
    dato_start = st.date_input("Fra dato:", value=df["Dato"].min() if not df.empty else datetime.today())
    dato_slutt = st.date_input("Til dato:", value=df["Dato"].max() if not df.empty else datetime.today())

    filtered_df = df.copy()

    if type_filter != "Alle":
        filtered_df = filtered_df[filtered_df["Type"] == type_filter]
    
    if kategori_filter:
        filtered_df = filtered_df[filtered_df["Kategori"].str.contains(kategori_filter, case=False)]
    
    filtered_df = filtered_df[(filtered_df["Dato"] >= pd.to_datetime(dato_start)) & 
                              (filtered_df["Dato"] <= pd.to_datetime(dato_slutt))]

    st.markdown("## 📄 Dine transaksjoner")

for _, row in filtered_df.iterrows():
    with st.expander(f"{row['Dato'].strftime('%Y-%m-%d')} – {row['Kategori']} – {row['Beløp']} kr"):
        st.write(f"**Type:** {row['Type']}")
        st.write(f"**Kategori:** {row['Kategori']}")
        st.write(f"**Beløp:** {row['Beløp']} kr")
        st.write(f"**Saldo etter:** {row['Saldo']} kr")
        if st.button(f"🗑️ Slett transaksjon {row['id']}", key=f"slett_{row['id']}"):
            slett_transaksjon(row['id'])
            st.success("Transaksjon slettet.")
            st.experimental_rerun()



# 📊 Analyse
elif valg == "📊 Analyse":
    st.markdown("## 📊 Budsjettanalyse")
    inntekt, utgift = calculate_totals(df)
    col1, col2 = st.columns(2)
    col1.metric("Totale inntekter", f"{inntekt:.2f} kr")
    col2.metric("Totale utgifter", f"{utgift:.2f} kr")
    tips, level = generate_savings_tip(inntekt, utgift)
    getattr(st, level)(tips)

# 📈 Grafer
elif valg == "📈 Grafer":
    st.markdown("## 📈 Visualisering")
    plot_expense_bar(df)
    plot_pie_chart(df[df["Type"] == "Utgift"].groupby("Kategori")["Beløp"].sum())
    plot_saldo(df)

# 🔮 Prediksjon
elif valg == "🔮 Prediksjon":
    st.markdown("## 🔮 Prediksjon av saldo")
    dato_null, trend = predict_zero_balance(df)
    if dato_null:
        st.warning(f"Saldoen vil nå 0 kr rundt {dato_null}.")
    else:
        st.success("Saldoen ser ut til å holde seg stabil eller øke.")

# 📥 PDF-rapport
elif valg == "📥 PDF-rapport":
    st.markdown("## 📥 Generer PDF-rapport")
    if st.button("Generer PDF"):
        df["Uke"] = df["Dato"].dt.isocalendar().week
        ukesaldo = df.groupby("Uke")["Saldo"].last()
        ukekategorier = df[df["Type"] == "Utgift"].groupby(["Uke", "Kategori"])["Beløp"].sum().unstack(fill_value=0)
        prediksjonstekst = f"Saldoen vil nå 0 kr rundt {dato_null}" if dato_null else "Saldoen ser stabil ut."
        pdf = generate_pdf(df, df["Saldo"].iloc[-1], prediksjonstekst, ukesaldo, ukekategorier)
        st.download_button("📥 Last ned PDF", data=pdf.output(dest="S").encode("latin-1"), file_name="studentbudsjett_rapport.pdf")

# ➕ Legg til transaksjon
elif valg == "➕ Legg til transaksjon":
    st.markdown("## ➕ Legg til ny transaksjon")
    submitted = False
    with st.form("ny_transaksjon"):
        dato = st.date_input("Dato", value=datetime.today())
        type_ = st.selectbox("Type", ["Inntekt", "Utgift"])
        beløp = st.number_input("Beløp", min_value=0.0, step=100.0)
        kategori = st.text_input("Kategori")
        submit = st.form_submit_button("Legg til")

        if submit and kategori:
            insert_transaksjon(dato, type_, beløp, kategori)
            submitted = True


    if submitted:
        st.success("Transaksjon lagt til!")
        if st.button("🔄 Oppdater visning"):
            st.experimental_rerun()


