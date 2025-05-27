from fastapi import APIRouter
from pydantic import BaseModel
import psycopg2
import os

router = APIRouter()

class SelloutData(BaseModel):
    reference: str
    location: str
    date: str
    time: str
    price: float
    serial_number: str | None = None
    brand: str

@router.post("/insert")
def insert_data(data: SelloutData):
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sellout_data (
                id SERIAL PRIMARY KEY,
                reference TEXT,
                location TEXT,
                date DATE,
                time TIME,
                price FLOAT,
                serial_number TEXT,
                brand TEXT
            )
        """)
        cur.execute("""
            INSERT INTO sellout_data (reference, location, date, time, price, serial_number, brand)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.reference,
            data.location,
            data.date,
            data.time,
            data.price,
            data.serial_number,
            data.brand
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "details": str(e)}