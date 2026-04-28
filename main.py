from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv

# Cargamos variables de entorno
load_dotenv()

app = FastAPI()

# Configuración de CORS para que Vercel y Render se hablen sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    # Intenta usar la variable de entorno de Render, si no, usa la directa
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        db_url = "postgresql://automatas:Automatas2026*@76.13.229.191:5432/bases_de_datos"
    return psycopg2.connect(db_url)

# RUTA PRINCIPAL: Esto es lo que soluciona el "Not Found" en Vercel
@app.get("/")
async def read_index():
    return FileResponse('index.html')

# API de datos para el Dashboard
@app.get("/api/leads")
def get_leads():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Total histórico
        cur.execute("SELECT COUNT(*) FROM registro_leads")
        total = cur.fetchone()[0]

        # Total de hoy
        cur.execute(
            "SELECT COUNT(*) FROM registro_leads WHERE fecha::date = CURRENT_DATE"
        )
        today = cur.fetchone()[0]

        cur.close()
        conn.close()

        return {"total": total, "today": today}
    except Exception as e:
        return {"error": str(e), "total": 0, "today": 0}
