import csv
import os
from typing import Callable, List, Dict, Optional
from bs4 import BeautifulSoup
from fastapi import HTTPException
import requests

from app.core.constants import DATA_DIR

def validate_year(year: int, start_year: int, end_year: int):
    if year < start_year or year > end_year:
        raise HTTPException(
            status_code=400,
            detail=f"Year out of range. Available range: {start_year} to {end_year}"
        )

def validate_category(category: str, allowed_categories: list[str]):
    if category not in allowed_categories:
        available = ", ".join(allowed_categories)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Available categories: {available}"
        )

def load_from_csv(
    csv_path: str,
    year: int,
    columns: List[str],
) -> List[Dict[str, str]]:
    year_str = str(year)
    result = []


    full_csv_path = os.path.join(DATA_DIR, csv_path)

    with open(full_csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        header = next(reader)

        fixed_col_indices = {col: i for i, col in enumerate(header) if col in columns}
        year_indices = [i for i, col in enumerate(header) if col == year_str]

        if not year_indices:
            return []

        for row in reader:
            if all(not row[i].strip() for i in year_indices):
                continue

            item = {}

            for col, i in fixed_col_indices.items():
                item[col] = row[i].strip()

            for idx, i in enumerate(year_indices):
                col_name = year_str if len(year_indices) == 1 else f"{year_str}_{idx+1}"
                item[col_name] = row[i].strip()

            result.append(item)
            
    return result

def scrape_table_data_from_site(
    url: str,
    year: int,
    parse_row_fn: Callable[[list, int], Optional[dict]],
    expected_col_range: tuple[int, int]
) -> list[dict]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        raise ValueError("Data table not found")

    rows = table.find("tbody").find_all("tr")
    data = []

    for tr in rows:
        columns = tr.find_all("td")
        if not expected_col_range[0] <= len(columns) <= expected_col_range[1]:
            continue

        parsed = parse_row_fn(columns, year)
        if parsed:
            data.append(parsed)

    return data