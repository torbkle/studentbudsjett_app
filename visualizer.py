import matplotlib.pyplot as plt
import streamlit as st

def plot_expense_bar(df):
    fig, ax = plt.subplots()
    df.groupby("Kategori")["Beløp"].sum().plot(kind="bar", ax=ax)
    ax.set_title("Utgifter per kategori")
    st.pyplot(fig)

def plot_saldo(df_sorted):
    fig, ax = plt.subplots()
    ax.plot(df_sorted["Dato"], df_sorted["Saldo"], marker="o", linestyle="-", color="teal")
    ax.set_title("Saldo over tid")
    ax.set_xlabel("Dato")
    ax.set_ylabel("Saldo (kr)")
    ax.grid(True)
    st.pyplot(fig)

def plot_pie_chart(kategori_sum):
    fig, ax = plt.subplots()
    ax.pie(kategori_sum, labels=kategori_sum.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Fordeling av utgifter")
    st.pyplot(fig)
