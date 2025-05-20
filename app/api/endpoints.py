from fastapi import APIRouter, HTTPException

from app.core.constants import IMPORT_CATEGORY_MAP, END_IMPORT_YEAR, START_IMPORT_YEAR
from app.scraping.import_tab import get_import_data

router = APIRouter()

@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}

@router.get("/import/{category}/{year}")
async def get_import_data_by_category_year(category: str, year: int):
    if category not in IMPORT_CATEGORY_MAP:
        available_categories = ", ".join(IMPORT_CATEGORY_MAP.keys())
        raise HTTPException(status_code=400, detail=f"Invalid category. Available categories: {available_categories}")
    if year < START_IMPORT_YEAR or year > END_IMPORT_YEAR:
        raise HTTPException(status_code=400, detail=f"Year out of range. Available range: {START_IMPORT_YEAR} to {END_IMPORT_YEAR}")
    
    return get_import_data(category, year)
