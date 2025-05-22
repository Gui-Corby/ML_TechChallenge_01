from fastapi import APIRouter, HTTPException
from app.scraping.functions.drinks import drinks_scraping
from app.scraping.functions.csv_callback import csv_callback
from app.core.utils import validate_year
from app.core.constants import START_YEAR, END_YEAR
import tracemalloc
from app.scraping.production import URL_TEMPLATE
tracemalloc.start()

router = APIRouter()


@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}


# Endpoint to get production data for a specific year.
@router.get("/production/{year}", summary="Import data for a specific year")
async def get_production_data(year: int):
    """
    Returns production data for a specific year.
    """
    try:
        validate_year(year, START_YEAR, END_YEAR - 1)
        data = drinks_scraping(URL_TEMPLATE, year)
        return data
    except HTTPException as e:
        # Re-raise HTTPExceptions so they propagate as intended.
        raise e

    except Exception:
        data = csv_callback(year)
        return data
