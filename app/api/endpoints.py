from fastapi import APIRouter, HTTPException
from ..scraping.production import scrape_production_data_from_site
from ..scraping.functions.csv_callback import csv_callback
from ..core.utils import validate_year
from ..core.constants import START_YEAR, END_YEAR
from ..core.constants import PRODUCTION_BASE_URL as URL_TEMPLATE
import tracemalloc
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
        data = scrape_production_data_from_site(URL_TEMPLATE, year)
        return data
    except HTTPException as e:
        raise e

    except Exception:
        data = csv_callback(year)
        return data
