from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles # <--- NUEVO
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

# ESTA LÍNEA ES LA CLAVE: Le dice a FastAPI que la carpeta /static contiene archivos reales
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        db_url = "postgresql://automatas:Automatas2026*@76.13.229.191:5432/bases_de_datos"
    return psycopg2.connect(db_url)

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/api/leads")
def get_leads():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM registro_leads")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM registro_leads WHERE fecha::date = CURRENT_DATE")
        today = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {"total": total, "today": today}
    except Exception as e:
        return {"error": str(e), "total": 0, "today": 0}
