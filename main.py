from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    # TEST DIRECTO: Ponemos la URL explícitamente para saltarnos el .env
    url_directa = "postgresql://automatas:Automatas2026*@76.13.229.191:5432/bases_de_datos"
    return psycopg2.connect(url_directa)

@app.get("/api/leads")
def get_leads():
    conn = get_db_connection()
    cur = conn.cursor()

    # Total histórico
    cur.execute("SELECT COUNT(*) FROM registro_leads")
    total = cur.fetchone()[0]

    # Total de hoy (¡Corregido a 'fecha'!)
    cur.execute(
        "SELECT COUNT(*) FROM registro_leads WHERE fecha::date = CURRENT_DATE"
    )
    today = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {"total": total, "today": today}
