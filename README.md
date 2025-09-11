# 📊 StudentBudsjett

StudentBudsjett er en mobilvennlig og brukervennlig budsjettapp for studenter, bygget med Streamlit og SQLite. Appen lar deg registrere inntekter og utgifter, visualisere saldo og utgiftsmønstre, og generere PDF-rapporter. Den er designet for enkel bruk både på mobil og desktop, og gir innsikt i økonomien din på en oversiktlig måte.

---

## 🚀 Kom i gang

### 1. Klon repoet

```bash
git clone https://github.com/torbkle/studentbudsjett_app.git
cd studentbudsjett_app
2. Installer avhengigheter
bash
pip install -r requirements.txt
3. Start appen
bash
streamlit run app.py
Appen åpnes automatisk i nettleseren din.

🧰 Funksjoner
➕ Legg til inntekter og utgifter med dato, type og kategori

📄 Se oversikt over alle transaksjoner

📊 Analyser total inntekt og utgift med sparetips

📈 Visualiser utgifter per kategori og saldo over tid

🔮 Prediksjon av når saldoen når 0 kr basert på trend

📥 Generer PDF-rapport med ukesoversikt og grafer

📱 Mobilvennlig layout med navigasjonsmeny

🗃️ Teknisk oversikt
Teknologi	Beskrivelse
Streamlit	Interaktiv webapp med sidebar og grafikk
SQLite	Lokal database for lagring av transaksjoner
Pandas	Dataanalyse og filtrering
Matplotlib	Grafer og visualisering
ReportLab	PDF-generering med ukesrapporter
📦 Filstruktur
Code
studentbudsjett_app/
├── app.py               # Hovedapplikasjon
├── db_handler.py        # SQLite-håndtering
├── analyzer.py          # Budsjettanalyse og sparetips
├── visualizer.py        # Grafer og diagrammer
├── predictor.py         # Prediksjon av saldo
├── pdf_report.py        # PDF-generering
├── requirements.txt     # Avhengigheter
└── README.md            # Dokumentasjon
🌐 Demo
Test appen direkte via Streamlit Cloud: Åpne StudentBudsjett-demoen

📄 Lisens
Dette prosjektet er åpent og fritt å bruke for læring og personlig bruk. Du står fritt til å tilpasse og forbedre det.

🙋‍♂️ Bidrag
Har du forslag, feilrapporter eller ønsker å bidra? Send gjerne en pull request eller kontakt torbjoernkleiven@gmail.com


