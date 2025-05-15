from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import json
from pathlib import Path

router = APIRouter()


@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}


# Endpoint to get production data for a specific year.
@router.get("/production/{year}")
async def get_production_data(year: int):
    # Checking if json file exists

    json_path = Path(__file__).parents[1] / "scraping" / "productions.json"
    if not json_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Data file not found")

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Filtering the data for the specified year
    filtered_data = [item for item in data if item.get("ano") == year]
    filtered_data = [
        {
            "categoria": item["categoria"],
            "bebida": item["bebida"],
            "quantidade(L)": item["quantidade(L)"]
        }
        for item in filtered_data
    ]

    # Removing 'bebida' key if it's the same as 'categoria', avoiding redundancy
    # and renaming 'quantidade(L)' to 'quantidade(L) total'
    for dict in filtered_data:
        if dict['categoria'] == dict['bebida']:
            del dict['bebida']
            dict['quantidade(L) total'] = dict['quantidade(L)']
            del dict['quantidade(L)']

    if not filtered_data:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for year {year}")

    # Returning the filtered data as a JSON response in a pretty format
    return JSONResponse(content=json.loads(json.dumps(
        filtered_data,
        indent=4,
        ensure_ascii=False
    )))
