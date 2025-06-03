from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
import logging

from app.core.constants import PROCESSING_START_YEAR, PROCESSING_END_YEAR, PROCESSING_CATEGORY_MAP
from app.core.utils import validate_category, validate_year
from app.scraping.processing_tab import format_processing_data, get_processing_data

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/{category}/{year}",
    summary="Processing data by category and year",
    description=f"""
    Retrieve processing data for a **specific category and year**.

    - **category**: Must be one of: {", ".join(PROCESSING_CATEGORY_MAP.keys())}
    - **year**: Must be between {PROCESSING_START_YEAR} and {PROCESSING_END_YEAR}

    Optional query parameters:
    - `offset`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return (default: 100, max: 1000).

    Returns formatted processing data, or a 204 status code if no data exists.
    """,
    response_description="List of formatted processing data",
    responses={
        200: {"description": "Export data retrieved successfully."},
        204: {"description": "No processing data available for the given category and year."},
        400: {"description": "Invalid category or year."},
        500: {"description": "Internal server error while retrieving processing data."}
    }
)
async def get_processing_data_by_category_year(
    category: Annotated[str, Path(description="Category of the data to processing")],
    year: Annotated[int, Path(description=f"Year between {PROCESSING_START_YEAR} and {PROCESSING_END_YEAR}")],
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
):
    """
    Get formatted processing data for a specific category and year.
    """
    allowed_categories = list(PROCESSING_CATEGORY_MAP)

    logger.info(f"Request: Processing data for category='{category}', year={year}")

    try:
        validate_category(category, allowed_categories)
        validate_year(year, PROCESSING_START_YEAR, PROCESSING_END_YEAR)
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    data = get_processing_data(category, year)
    if data is None:
        logger.error(f"Failed to retrieve raw processing data for category='{category}', year={year}")
        raise HTTPException(status_code=500, detail="Failed to retrieve processing data.")

    formatted = format_processing_data(data, year)

    if not formatted:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    paginated_data = formatted[offset:offset + limit]
    return paginated_data

@router.get(
    "/all",
    summary="Processing data for all categories and years",
    description=f"""
    Retrieve processing data for **all supported categories and years**.

    Iterates from {PROCESSING_START_YEAR} to {PROCESSING_END_YEAR} for each category:
    {", ".join(PROCESSING_CATEGORY_MAP.keys())}

    Optional query parameters:
    - `offset`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return (default: 100, max: 1000).
    """,
    response_description="List of all formatted processing data",
    responses={
        200: {"description": "All processing data retrieved successfully."},
        204: {"description": "No processing data available for any category or year."},
        500: {"description": "Internal server error while retrieving processing data."}
    }
)
async def get_all_export_data(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
):
    """
    Get all available processing data across all valid categories and years.
    """
    allowed_categories = list(PROCESSING_CATEGORY_MAP)
    all_data = []

    logger.info("Starting full processing data retrieval.")

    for category in allowed_categories:
        for year in range(PROCESSING_START_YEAR, PROCESSING_END_YEAR + 1):
            try:
                data = get_processing_data(category, year)
                if data is None:
                    continue

                formatted = format_processing_data(
                    data,
                    year,
                    category=PROCESSING_CATEGORY_MAP[category]["name"],
                    include_year_and_category=True
                )
                all_data.extend(formatted)
            except Exception as e:
                logger.warning(f"Error processing category='{category}', year={year}: {e}")
                continue

    if not all_data:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    paginated_data = all_data[offset:offset + limit]
    return paginated_data
