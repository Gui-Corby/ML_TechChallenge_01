from fastapi import APIRouter
from app.scraping.functions.drinks import drinks_scraping
from app.scraping.functions.csv_callback import csv_callback
import tracemalloc
from app.scraping.production import URL
tracemalloc.start()

router = APIRouter()


@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}


# Endpoint to get production data for a specific year.
@router.get("/production/{year}")
async def get_production_data(year: int):
    try:
        data = drinks_scraping(URL, year)
        return data

    except Exception:
        data = csv_callback(year)
        return data
