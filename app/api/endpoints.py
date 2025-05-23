from fastapi import APIRouter, HTTPException
import tracemalloc
from ..scraping.production import get_production_data
from ..core.utils import validate_year
from ..core.constants import START_YEAR, END_YEAR
tracemalloc.start()

router = APIRouter()


@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}


# Endpoint to get production data for a specific year.
@router.get("/production/{year}", summary="Import data for a specific year")
async def get_production_data_by_year(year: int):
    """
    Returns production data for a specific year.
    """
    try:
        validate_year(year, START_YEAR, END_YEAR - 1)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = get_production_data(year)
    if data is None:
        raise HTTPException(status_code=500,
                            detail="Failed to retrieve production data")
    return data
