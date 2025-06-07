from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

router = APIRouter()

# Schéma de données attendu
class Sale(BaseModel):
    brand: str
    model: str
    sold_at: datetime
    price: float
    country: str

# Connexion PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

@router.post("/insert")
def insert_sale(sale: Sale):
    try:
        conn = psycopg2.connect(DATABASE_URL)
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
        return {"message": "Sale inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
