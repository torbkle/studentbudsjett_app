from fpdf import FPDF
import datetime
import pandas as pd
from predictor import lag_prediksjonstekst
from ukeanalyse import ukesaldo, ukekategorier

from db_handler import hent_saldo

def generate_pdf(df, saldo, prediksjonstekst, ukesaldo, ukekategorier):
    pdf = FPDF()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.add_page()

    pdf.cell(200, 10, txt="StudentBudsjett Rapport", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Dato: {datetime.date.today()}", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Nåværende saldo: {saldo:.2f} kr", ln=True)
    pdf.cell(200, 10, txt=prediksjonstekst, ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Transaksjoner:", ln=True)
    for index, row in df.iterrows():
        linje = f"{row['Dato'].date()} | {row['Type']} | {row['Beløp']} kr | {row['Kategori']}"
        pdf.cell(200, 8, txt=linje, ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Ukentlig saldo:", ln=True)
    for uke, s in ukesaldo.items():
        pdf.cell(200, 8, txt=f"Uke {uke}: {s:.2f} kr", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Utgifter per kategori:", ln=True)
    for uke in ukekategorier.index:
        pdf.cell(200, 8, txt=f"Uke {uke}:", ln=True)
        for kategori, beløp in ukekategorier.loc[uke].items():
            pdf.cell(200, 8, txt=f" {kategori}: {beløp:.2f} kr", ln=True)

    return pdf

def lag_pdf_rapport(df):
    saldo = hent_saldo(df)
    prediksjonstekst = lag_prediksjonstekst(df)
    saldo_per_uke = ukesaldo(df)
    kategorier_per_uke = ukekategorier(df)

    pdf = generate_pdf(df, saldo, prediksjonstekst, saldo_per_uke, kategorier_per_uke)
    pdf.output("rapport.pdf")
