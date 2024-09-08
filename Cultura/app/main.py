from fastapi import FastAPI
from app.routers import products
from app.database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(products.router, prefix="/produtos", tags=["produtos"])



