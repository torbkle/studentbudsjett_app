import sqlite3
import pandas as pd

DB_PATH = "studentbudsjett.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transaksjoner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Dato TEXT,
            Type TEXT,
            Beløp REAL,
            Kategori TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_transaksjon(dato, type_, beløp, kategori):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO transaksjoner (Dato, Type, Beløp, Kategori)
        VALUES (?, ?, ?, ?)
    """, (dato, type_, beløp, kategori))
    conn.commit()
    conn.close()

def hent_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM transaksjoner ORDER BY Dato", conn, parse_dates=["Dato"])
    conn.close()
    return df
    
def slett_transaksjon(transaksjon_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM transaksjoner WHERE id = ?", (transaksjon_id,))
    conn.commit()
    conn.close()
    
def tøm_database():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM transaksjoner")
    conn.commit()
    conn.close()
