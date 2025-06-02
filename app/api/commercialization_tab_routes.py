from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
import logging

from app.core.constants import COMMERCIALIZATION_START_YEAR, COMMERCIALIZATION_END_YEAR
from app.core.utils import validate_year
from app.scraping.commercialization_tab import format_commercialization_data, get_commercialization_data

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/{year}",
    summary="Commercialization data by year",
    description=f"""
    Retrieve commercialization data for a **specific year**.
    
    - **year**: Must be between {COMMERCIALIZATION_START_YEAR} and {COMMERCIALIZATION_END_YEAR}

    Optional query parameters:
    - `offset`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return (default: 100, max: 1000).

    Returns formatted commercialization data, or a 204 status code if no data exists.
    """,
    response_description="List of formatted commercialization data",
    responses={
        200: {"description": "Commercialization data retrieved successfully."},
        204: {"description": "No commercialization data available for the year."},
        400: {"description": "Invalid year."},
        500: {"description": "Internal server error while retrieving commercialization data."}
    }
)
async def get_commercialization_data_by_year(
    year: Annotated[int, Path(description=f"Year between {COMMERCIALIZATION_START_YEAR} and {COMMERCIALIZATION_END_YEAR}")],
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
):
    """
    Get formatted commercialization data for a specific year.
    """
    logger.info(f"Request: Commercialization data for year={year}")

    try:
        validate_year(year, COMMERCIALIZATION_START_YEAR, COMMERCIALIZATION_END_YEAR)
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    data = get_commercialization_data(year)
    if data is None:
        logger.error(f"Failed to retrieve raw commercialization data for year={year}")
        raise HTTPException(status_code=500, detail="Failed to retrieve commercialization data.")

    formatted = format_commercialization_data(data, year)

    if not formatted:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    paginated_data = formatted[offset:offset + limit]
    return paginated_data

@router.get(
    "/all",
    summary="Commercialization data for all years",
    description=f"""
    Retrieve Commercialization data for **all supported years**.

    Iterates from {COMMERCIALIZATION_START_YEAR} to {COMMERCIALIZATION_END_YEAR}

    Optional query parameters:
    - `offset`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return (default: 100, max: 1000).
    """,
    response_description="List of all formatted commercialization data",
    responses={
        200: {"description": "All commercialization data retrieved successfully."},
        204: {"description": "No commercialization data available for any year."},
        500: {"description": "Internal server error while retrieving commercialization data."}
    }
)
async def get_all_commercialization_data(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
):
    """
    Get all available commercialization data across all valid years.
    """
    all_data = []

    logger.info("Starting full commercialization data retrieval.")

    for year in range(COMMERCIALIZATION_START_YEAR, COMMERCIALIZATION_END_YEAR + 1):
        try:
            data = get_commercialization_data(year)
            if data is None:
                continue

            formatted = format_commercialization_data(
                data,
                year,
                include_year=True
            )
            all_data.extend(formatted)
        except Exception as e:
            logger.warning(f"Error processing year={year}: {e}")
            continue

    if not all_data:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    paginated_data = all_data[offset:offset + limit]
    return paginated_data
