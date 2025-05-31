import csv
import os
from typing import List, Dict
from fastapi import HTTPException

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