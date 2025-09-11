import streamlit as st
from pdf_report import lag_pdf_rapport
from components.infoboks import vis_infoboks
from components.tabell import vis_tabell


def vis(df):
    st.markdown("## 📥 PDF-rapport")

    try:
        saldo = df["Saldo"].iloc[-1]
        vis_infoboks("Nåværende saldo", f"{saldo:.2f} kr", ikon="💰", farge="#2E8B57")

        from predictor import lag_prediksjonstekst
        prediksjon = lag_prediksjonstekst(df)
        vis_infoboks("Prediksjon", prediksjon, ikon="🔮", farge="#4682B4")

        vis_tabell(df, tittel="Siste transaksjoner")

        lag_pdf_rapport(df)
        with open("rapport.pdf", "rb") as f:
            st.download_button("📄 Last ned PDF", f, file_name="StudentBudsjett_Rapport.pdf")

        st.success("PDF generert!")
    except Exception as e:
        st.error(f"Feil under PDF-generering: {e}")

