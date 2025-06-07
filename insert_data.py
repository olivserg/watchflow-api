import os
import psycopg2
from psycopg2.extensions import parse_dsn
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Sale(BaseModel):
    brand: str
    model: str
    sold_at: datetime
    price: float
    country: str

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
print("DATABASE_URL:", repr(DATABASE_URL))

@router.post("/insert")
def insert_sale(sale: Sale):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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
        return {"error": str(e)}
