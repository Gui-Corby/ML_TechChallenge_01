from fastapi import APIRouter, HTTPException
import logging

from ..scraping.production import get_production_data, format_production_data
from ..core.utils import validate_year
from ..core.constants import START_YEAR, END_YEAR


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}


# Endpoint to get production data for a specific year.
@router.get("/production/{year}", summary="Import data for a specific year")
async def get_production_data_by_year(
    year: int,
    limit: int | None = None,
    offset: int | None = None
):
    """
    Returns production data for a specific year, optionally paginated.
    """
    try:
        validate_year(year, START_YEAR, END_YEAR - 1)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    is_scraped, data = get_production_data(year)

    if not data:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve production data"
        )

    if not is_scraped:
        data = format_production_data(data, year)

    if offset:
        data = data[offset:]
    if limit:
        data = data[:limit]

    return data
