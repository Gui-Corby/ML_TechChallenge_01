from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from app.core.constants import COMMERCIALIZATION_START_YEAR, COMMERCIALIZATION_END_YEAR, IMPORT_CATEGORY_MAP, END_IMPORT_YEAR, START_IMPORT_YEAR
from app.core.utils import validate_category, validate_year
from app.scraping.commercialization_tab import format_commercialization_data, get_commercialization_data
from app.scraping.import_tab import format_import_data, get_import_data

logger = logging.getLogger(__name__)
router = APIRouter()


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
        validate_year(year, COMMERCIALIZATION_START_YEAR, COMMERCIALIZATION_END_YEAR - 1)
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

@router.get("/import/{category}/{year}", summary="Import data by category and year")
async def get_import_data_by_category_year(category: str, year: int):
    """
    Returns import data for a given category and year.
    """
    allowed_categories = list(IMPORT_CATEGORY_MAP)

    try:
        validate_category(category, allowed_categories)
        validate_year(year, START_IMPORT_YEAR, END_IMPORT_YEAR)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = get_import_data(category, year)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve import data.")

    formatted = format_import_data(data, year)

    if not formatted:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    return formatted


@router.get("/import/all", summary="Import data for all categories and years")
async def get_all_import_data():
    """
    Returns all available import data across all categories and years.
    """
    allowed_categories = list(IMPORT_CATEGORY_MAP)
    all_data = []

    for category in allowed_categories:
        for year in range(START_IMPORT_YEAR, END_IMPORT_YEAR + 1):
            try:
                data = get_import_data(category, year)
                if data is None:
                    logger.warning(f"Data not found '{category}', year '{year}': {e}")
                    continue

                formatted = format_import_data(
                            data,
                            year,
                            category=IMPORT_CATEGORY_MAP[category]["name"],
                            include_year_and_category=True
                        )
                all_data.extend(formatted)
            except Exception as e:
                logger.warning(f"Error while processing category '{category}', year '{year}': {e}")
                continue

    if not all_data:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    return all_data
