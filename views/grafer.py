import streamlit as st
from visualizer import plot_expense_bar, plot_pie_chart, plot_saldo

def vis(df):
    st.markdown("## 📈 Visualisering")
    plot_expense_bar(df)
    plot_pie_chart(df[df["Type"] == "Utgift"].groupby("Kategori")["Beløp"].sum())
    plot_saldo(df)
