from sklearn.linear_model import LinearRegression
import pandas as pd

def predict_zero_balance(df_sorted):
    df_sorted["Dag"] = (df_sorted["Dato"] - df_sorted["Dato"].min()).dt.days
    X = df_sorted[["Dag"]]
    y = df_sorted["Saldo"]
    model = LinearRegression()
    model.fit(X, y)
    if model.coef_[0] < 0:
        dag_null = -model.intercept_ / model.coef_[0]
        dato_null = df_sorted["Dato"].min() + pd.Timedelta(days=dag_null)
        return dato_null.date(), model.coef_[0]
    else:
        return None, model.coef_[0]

def lag_prediksjonstekst(df):
    df_sorted = df.sort_values("Dato")
    dato_null, trend = predict_zero_balance(df_sorted)
    if dato_null:
        return f"Saldoen forventes å nå 0 kr rundt {dato_null} (trend: {trend:.2f} kr/dag)"
    else:
        return f"Saldoen øker eller er stabil (trend: {trend:.2f} kr/dag)"
