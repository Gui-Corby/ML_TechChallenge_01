from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
import logging

from app.core.constants import EXPORT_START_YEAR, EXPORT_END_YEAR, EXPORT_CATEGORY_MAP
from app.core.utils import validate_category, validate_year
from app.scraping.export_tab import format_export_data, get_export_data

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/{category}/{year}",
    summary="Export data by category and year",
    description=f"""
    Retrieve export data for a **specific category and year**.

    - **category**: Must be one of: {", ".join(EXPORT_CATEGORY_MAP.keys())}
    - **year**: Must be between {EXPORT_START_YEAR} and {EXPORT_END_YEAR}

    Optional query parameters:
    - `offset`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return (default: 100, max: 1000).

    Returns formatted export data, or a 204 status code if no data exists.
    """,
    response_description="List of formatted export data",
    responses={
        200: {"description": "Export data retrieved successfully."},
        204: {"description": "No export data available for the given category and year."},
        400: {"description": "Invalid category or year."},
        500: {"description": "Internal server error while retrieving export data."}
    }
)
async def get_export_data_by_category_year(
    category: Annotated[str, Path(description="Category of the data to export")],
    year: Annotated[int, Path(description=f"Year between {EXPORT_START_YEAR} and {EXPORT_END_YEAR}")],
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
):
    """
    Get formatted export data for a specific category and year.
    """
    allowed_categories = list(EXPORT_CATEGORY_MAP)

    logger.info(f"Request: Export data for category='{category}', year={year}")

    try:
        validate_category(category, allowed_categories)
        validate_year(year, EXPORT_START_YEAR, EXPORT_END_YEAR)
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    data = get_export_data(category, year)
    if data is None:
        logger.error(f"Failed to retrieve raw export data for category='{category}', year={year}")
        raise HTTPException(status_code=500, detail="Failed to retrieve export data.")

    formatted = format_export_data(data, year)

    if not formatted:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    paginated_data = formatted[offset:offset + limit]
    return paginated_data

@router.get(
    "/all",
    summary="Export data for all categories and years",
    description=f"""
    Retrieve export data for **all supported categories and years**.

    Iterates from {EXPORT_START_YEAR} to {EXPORT_END_YEAR} for each category:
    {", ".join(EXPORT_CATEGORY_MAP.keys())}

    Optional query parameters:
    - `offset`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return (default: 100, max: 1000).
    """,
    response_description="List of all formatted export data",
    responses={
        200: {"description": "All export data retrieved successfully."},
        204: {"description": "No export data available for any category or year."},
        500: {"description": "Internal server error while retrieving export data."}
    }
)
async def get_all_export_data(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
):
    """
    Get all available export data across all valid categories and years.
    """
    allowed_categories = list(EXPORT_CATEGORY_MAP)
    all_data = []

    logger.info("Starting full export data retrieval.")

    for category in allowed_categories:
        for year in range(EXPORT_START_YEAR, EXPORT_END_YEAR + 1):
            try:
                data = get_export_data(category, year)
                if data is None:
                    continue

                formatted = format_export_data(
                    data,
                    year,
                    category=EXPORT_CATEGORY_MAP[category]["name"],
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
