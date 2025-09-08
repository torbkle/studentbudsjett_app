import streamlit as st
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from fpdf import FPDF

# 📌 Logo og introduksjon
st.image("studentbudsjett_logo.png", width=200)
st.title("StudentBudsjett 2.0")
st.write("Få oversikt over økonomien din – uke for uke.")

# 📋 Registrering
st.sidebar.header("Legg til transaksjon")
trans_type = st.sidebar.selectbox("Type", ["Inntekt", "Utgift"])
amount = st.sidebar.number_input("Beløp (kr)", min_value=0.0, step=10.0)
category = st.sidebar.selectbox("Kategori", ["Mat", "Bolig", "Transport", "Fritid", "Annet"])
date = st.sidebar.date_input("Dato", value=datetime.date.today())

if st.sidebar.button("Legg til"):
    new_data = {"Dato": date, "Type": trans_type, "Beløp": amount, "Kategori": category}
    st.session_state.setdefault("transaksjoner", []).append(new_data)
    st.success("Transaksjon lagt til!")

# 📊 Analyse
df = pd.DataFrame(st.session_state.get("transaksjoner", []))
if not df.empty:
    df["Dato"] = pd.to_datetime(df["Dato"])
    df["Uke"] = df["Dato"].dt.isocalendar().week
    df["Beløp_signed"] = df.apply(lambda r: r["Beløp"] if r["Type"] == "Inntekt" else -r["Beløp"], axis=1)
    df_sorted = df.sort_values("Dato")
    df_sorted["Saldo"] = df_sorted["Beløp_signed"].cumsum()
    df_sorted["Dag"] = (df_sorted["Dato"] - df_sorted["Dato"].min()).dt.days

    st.subheader("📋 Transaksjoner")
    st.dataframe(df)

    # 📈 Saldoanalyse
    saldo = df_sorted["Saldo"].iloc[-1]
    st.metric("💰 Nåværende saldo", f"{saldo:.2f} kr")

    model = LinearRegression()
    model.fit(df_sorted[["Dag"]], df_sorted["Saldo"])
    if model.coef_[0] < 0:
        dag_null = -model.intercept_ / model.coef_[0]
        dato_null = df_sorted["Dato"].min() + pd.Timedelta(days=dag_null)
        st.warning(f"🔮 Du går tom for penger rundt {dato_null.date()}")
    else:
        st.success("🔮 Saldoen vokser – ingen fare for tom konto!")

    # 📊 Ukentlig oppsummering
    st.subheader("📅 Ukentlig saldoendring")
    ukesaldo = df.groupby("Uke")["Beløp_signed"].sum().cumsum()
    st.line_chart(ukesaldo)

    st.subheader("📊 Utgifter per kategori per uke")
    ukekategorier = df[df["Type"] == "Utgift"].groupby(["Uke", "Kategori"])["Beløp"].sum().unstack(fill_value=0)
    st.bar_chart(ukekategorier)

    # 💡 Tips
    if "Mat" in df["Kategori"].values and df[df["Kategori"] == "Mat"]["Beløp"].sum() > 1000:
        st.info("💡 Tips: Vurder å lage mat hjemme oftere for å redusere matutgifter.")

    # 📄 PDF-rapport
    pdf = FPDF()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.add_page()
    pdf.cell(200, 10, txt="StudentBudsjett Rapport", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Dato: {datetime.date.today()}", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Nåværende saldo: {saldo:.2f} kr", ln=True)
    if model.coef_[0] < 0:
        pdf.cell(200, 10, txt=f"Prediksjon: Tom for penger rundt {dato_null.date()}", ln=True)
    else:
        pdf.cell(200, 10, txt="Prediksjon: Saldoen vokser – ingen fare for tom konto!", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Ukentlig saldo:", ln=True)
    for uke, s in ukesaldo.items():
        pdf.cell(200, 8, txt=f"Uke {uke}: {s:.2f} kr", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Utgifter per kategori:", ln=True)
    for uke in ukekategorier.index:
        pdf.cell(200, 8, txt=f"Uke {uke}:", ln=True)
        for kategori, beløp in ukekategorier.loc[uke].items():
            pdf.cell(200, 8, txt=f"  {kategori}: {beløp:.2f} kr", ln=True)

    pdf_bytes = pdf.output(dest='S').encode('utf-8')
    st.download_button("📄 Last ned PDF-rapport", pdf_bytes, "studentbudsjett_rapport.pdf", "application/pdf", key="pdf_download")

else:
    st.info("Ingen transaksjoner registrert ennå.")
