import tracemalloc
from fastapi import APIRouter, HTTPException
from ..scraping.commercialization import get_commercialization_data, format_commercialization_data
from ..core.utils import validate_year
from ..core.constants import START_YEAR, END_YEAR

tracemalloc.start()

router = APIRouter()

@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}

# Endpoint to get commercialization data for a specific year.
@router.get("/commercialization/{year}", summary="Import data for a specific year")
async def get_commercialization_data_by_year(
    year: int,
    limit: int | None = None,
    offset: int | None = None
):
    """
    Returns commercialization data for a specific year.
    """
    try:
        validate_year(year, START_YEAR, END_YEAR - 1)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    is_scraped, data = get_commercialization_data(year)

    if not data:
        raise HTTPException(status_code=500,
                            detail="Failed to retrieve commercialization data")
    
    if not is_scraped:
        data = format_commercialization_data(data, year)
    
    if offset:
        data = data[offset:]
    if limit:
        data = data[:limit]
    
    return data
