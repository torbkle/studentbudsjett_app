import streamlit as st
import pandas as pd
from db_handler import slett_transaksjon
from datetime import datetime
from components.infoboks import vis_infoboks

def vis(df):
    saldo = df["Saldo"].iloc[-1]
    vis_infoboks("Nåværende saldo", f"{saldo:.2f} kr", ikon="💰", farge="#2E8B57")

    st.markdown("### 📋 Transaksjoner")
    st.dataframe(df, use_container_width=True)
    st.markdown("## 📄 Dine transaksjoner")
    st.info(f"Antall transaksjoner: {len(df)}")

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
