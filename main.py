from fastapi import FastAPI
from routers import insert_data

app = FastAPI()
app.include_router(insert_data.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to WatchFlow API"}