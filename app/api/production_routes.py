from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
import logging

from app.core.constants import PRODUCTION_START_YEAR, PRODUCTION_END_YEAR
from app.core.utils import validate_year
from app.scraping.production_tab import format_production_data, get_production_data

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/{year}",
    summary="Production data by year",
    description=f"""
    Retrieve production data for a **specific year**.
    
    - **year**: Must be between {PRODUCTION_START_YEAR} and {PRODUCTION_END_YEAR}

    Optional query parameters:
    - `offset`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return (default: 100, max: 1000).

    Returns formatted production data, or a 204 status code if no data exists.
    """,
    response_description="List of formatted production data",
    responses={
        200: {"description": "Production data retrieved successfully."},
        204: {"description": "No production data available for the year."},
        400: {"description": "Invalid year."},
        500: {"description": "Internal server error while retrieving production data."}
    }
)
async def get_production_data_by_year(
    year: Annotated[int, Path(description=f"Year between {PRODUCTION_START_YEAR} and {PRODUCTION_END_YEAR}")],
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
):
    """
    Get formatted production data for a specific year.
    """
    logger.info(f"Request: Production data for year={year}")

    try:
        validate_year(year, PRODUCTION_START_YEAR, PRODUCTION_END_YEAR)
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    data = get_production_data(year)
    if data is None:
        logger.error(f"Failed to retrieve raw production data for year={year}")
        raise HTTPException(status_code=500, detail="Failed to retrieve production data.")

    formatted = format_production_data(data, year)

    if not formatted:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    paginated_data = formatted[offset:offset + limit]
    return paginated_data

@router.get(
    "/all",
    summary="Production data for all years",
    description=f"""
    Retrieve Production data for **all supported years**.

    Iterates from {PRODUCTION_START_YEAR} to {PRODUCTION_END_YEAR}

    Optional query parameters:
    - `offset`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return (default: 100, max: 1000).
    """,
    response_description="List of all formatted production data",
    responses={
        200: {"description": "All production data retrieved successfully."},
        204: {"description": "No production data available for any year."},
        500: {"description": "Internal server error while retrieving production data."}
    }
)
async def get_all_production_data(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
):
    """
    Get all available production data across all valid years.
    """
    all_data = []

    logger.info("Starting full production data retrieval.")

    for year in range(PRODUCTION_START_YEAR, PRODUCTION_END_YEAR + 1):
        try:
            data = get_production_data(year)
            if data is None:
                continue

            formatted = format_production_data(
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
