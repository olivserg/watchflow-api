import os
import psycopg2
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Schéma de données attendu
class Sale(BaseModel):
    brand: str
    model: str
    sold_at: datetime
    price: float
    country: str

# Connexion PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

@router.post("/insert")
def insert_sale(sale: Sale):
    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL is not set")

    try:
        print(f"DATABASE_URL: {DATABASE_URL!r}")
        conn = psycopg2.connect(
    dbname="railway",
    user="postgres",
    password="IKABjccoetNZoGPAzNLCzQajvLlNbvVp",
    host="switchback.proxy.rlwy.net",
    port="53686"
)

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS watch_sales (
                id SERIAL PRIMARY KEY,
                brand TEXT,
                model TEXT,
                sold_at TIMESTAMP,
                price NUMERIC,
                country TEXT
            )
        """)

        cur.execute("""
            INSERT INTO watch_sales (brand, model, sold_at, price, country)
            VALUES (%s, %s, %s, %s, %s)
        """, (sale.brand, sale.model, sale.sold_at, sale.price, sale.country))

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Data inserted successfully"}

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
