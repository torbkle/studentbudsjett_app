import pandas as pd

def ukesaldo(df):
    df["Uke"] = df["Dato"].dt.isocalendar().week
    return df.groupby("Uke")["Saldo"].last().to_dict()

def ukekategorier(df):
    df["Uke"] = df["Dato"].dt.isocalendar().week
    utgifter = df[df["Type"] == "Utgift"]
    return utgifter.groupby(["Uke", "Kategori"])["Beløp"].sum().unstack(fill_value=0)
