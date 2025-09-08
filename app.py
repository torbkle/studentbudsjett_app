# app.py
import streamlit as st
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO


# 📌 Logo og introduksjon
st.image("studentbudsjett_logo.png", width=200)
st.write("Hold oversikt over inntekter og utgifter – og få prediksjon på når du går tom for penger.")

# 📋 Sidepanel for transaksjoner
st.sidebar.header("Legg til transaksjon")
trans_type = st.sidebar.selectbox("Type", ["Inntekt", "Utgift"])
amount = st.sidebar.number_input("Beløp (kr)", min_value=0.0, step=10.0)
category = st.sidebar.selectbox("Kategori", ["Mat", "Bolig", "Transport", "Fritid", "Annet"])
date = st.sidebar.date_input("Dato", value=datetime.date.today())

if st.sidebar.button("Legg til"):
    new_data = {"Dato": date, "Type": trans_type, "Beløp": amount, "Kategori": category}
    st.session_state.setdefault("transaksjoner", []).append(new_data)
    st.success("Transaksjon lagt til!")

# 📊 Vis transaksjoner og analyser
st.subheader("📋 Dine transaksjoner")
df = pd.DataFrame(st.session_state.get("transaksjoner", []))

if not df.empty:
    df["Dato"] = pd.to_datetime(df["Dato"])  # 🔧 Sikre riktig datoformat
    st.dataframe(df)

    # 💾 Last ned transaksjoner som CSV
    csv_trans = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Last ned transaksjoner (CSV)",
        data=csv_trans,
        file_name="studentbudsjett_transaksjoner.csv",
        mime="text/csv"
    )

    # 💰 Beregn saldo
    df["Beløp_signed"] = df.apply(lambda row: row["Beløp"] if row["Type"] == "Inntekt" else -row["Beløp"], axis=1)
    df_sorted = df.sort_values("Dato")
    df_sorted["Saldo"] = df_sorted["Beløp_signed"].cumsum()
    df_sorted["Dag"] = (df_sorted["Dato"] - df_sorted["Dato"].min()).dt.days

    saldo = df_sorted["Saldo"].iloc[-1]
    st.metric("💰 Nåværende saldo", f"{saldo:.2f} kr")

    # 🔮 Prediksjon: Når går du tom for penger?
    X = df_sorted[["Dag"]]
    y = df_sorted["Saldo"]
    model = LinearRegression()
    model.fit(X, y)

    if model.coef_[0] < 0:
        dag_null = -model.intercept_ / model.coef_[0]
        dato_null = df_sorted["Dato"].min() + pd.Timedelta(days=dag_null)
        st.warning(f"🔮 Prediksjon: Du går tom for penger rundt {dato_null.date()}")
    else:
        st.success("🔮 Prediksjon: Saldoen din vokser – ingen fare for tom konto!")

    # 📄 Generer PDF-rapport
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Tittel og dato
    pdf.cell(200, 10, txt="StudentBudsjett Rapport", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Dato: {datetime.date.today()}", ln=True, align="C")
    pdf.ln(10)

    # Saldo og prediksjon
    pdf.cell(200, 10, txt=f"Nåværende saldo: {saldo:.2f} kr", ln=True)
    if model.coef_[0] < 0:
        pdf.cell(200, 10, txt=f"Prediksjon: Tom for penger rundt {dato_null.date()}", ln=True)
    else:
        pdf.cell(200, 10, txt="Prediksjon: Saldoen vokser – ingen fare for tom konto!", ln=True)
    pdf.ln(10)

    # Transaksjonstabell
    pdf.cell(200, 10, txt="Transaksjoner:", ln=True)
    for index, row in df.iterrows():
        linje = f"{row['Dato'].date()} | {row['Type']} | {row['Beløp']} kr | {row['Kategori']}"
        pdf.cell(200, 8, txt=linje, ln=True)

    # Gjør PDF nedlastbar
    buffer = BytesIO()
    pdf.output(buffer)
    st.download_button(
        label="📄 Last ned budsjett som PDF",
        data=buffer.getvalue(),
        file_name="studentbudsjett_rapport.pdf",
        mime="application/pdf"
    )

    
    # 💾 Last ned saldohistorikk som CSV
    csv_saldo = df_sorted[["Dato", "Saldo"]].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Last ned saldohistorikk (CSV)",
        data=csv_saldo,
        file_name="studentbudsjett_saldo.csv",
        mime="text/csv"
    )

    # 📈 Visualiser saldoen over tid
    fig1, ax1 = plt.subplots()
    ax1.plot(df_sorted["Dato"], df_sorted["Saldo"], marker="o", linestyle="-", color="teal")
    ax1.set_title("Saldo over tid")
    ax1.set_xlabel("Dato")
    ax1.set_ylabel("Saldo (kr)")
    ax1.grid(True)
    st.pyplot(fig1)

    # 🥧 Kakediagram over utgifter per kategori
    utgifter = df[df["Type"] == "Utgift"]
    if not utgifter.empty:
        kategori_sum = utgifter.groupby("Kategori")["Beløp"].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(kategori_sum, labels=kategori_sum.index, autopct="%1.1f%%", startangle=90)
        ax2.set_title("Fordeling av utgifter")
        st.subheader("📊 Fordeling av utgifter")
        st.pyplot(fig2)

        # 💾 Last ned utgiftsfordeling som CSV
        csv_kategorier = kategori_sum.reset_index().to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Last ned utgiftsfordeling (CSV)",
            data=csv_kategorier,
            file_name="studentbudsjett_utgifter.csv",
            mime="text/csv"
        )

        # ⚠️ Advarsel hvis én kategori overstiger 50 % av utgiftene
        total_utgift = kategori_sum.sum()
        største_kategori = kategori_sum.idxmax()
        andel = kategori_sum.max() / total_utgift

        if andel > 0.5:
            st.error(f"⚠️ Advarsel: Kategori '{største_kategori}' utgjør {andel:.1%} av dine utgifter!")
        elif andel > 0.3:
            st.warning(f"🔎 Merk: Kategori '{største_kategori}' utgjør {andel:.1%} av dine utgifter.")

else:
    st.info("Ingen transaksjoner registrert ennå.")
