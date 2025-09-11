def calculate_totals(df):
    total_utgift = df[df["Type"] == "Utgift"]["Beløp"].sum()
    total_inntekt = df[df["Type"] == "Inntekt"]["Beløp"].sum()
    return total_inntekt, total_utgift

def generate_savings_tip(total_inntekt, total_utgift):
    if total_utgift > total_inntekt:
        return "Du bruker mer enn du tjener. Vurder å kutte ned på 'Fritid' eller 'Mat'.", "warning"
    else:
        return "Bra jobbet! Du har positiv balanse.", "success"
