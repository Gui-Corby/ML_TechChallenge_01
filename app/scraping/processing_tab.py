from typing import Optional
from app.core.constants import PROCESSING_BASE_URL, PROCESSING_CATEGORY_MAP, PROCESSING_CSV_COLUMNS
from app.core.utils import load_from_csv, scrape_table_data_from_site


def get_processing_data(category: str, year: int) -> list[dict]:
    config = PROCESSING_CATEGORY_MAP.get(category)
    url = PROCESSING_BASE_URL.format(year=year, suboption=config["suboption"])

    try:
        return scrape_table_data_from_site(
            url,
            year,
            parse_row_fn=parse_processing_row,
            expected_col_range=(2, 2)
        )
    except Exception:
        return load_from_csv(config["data_path"], year, PROCESSING_CSV_COLUMNS)

def parse_processing_row(columns, year: int) -> dict:
    cultivate = columns[0].get_text(strip=True)
    amount = columns[1].get_text(strip=True)

    return {
        "cultivar": cultivate,
        f"{year}": amount
    }

def format_processing_data(
    data: list[dict],
    year: int,
    category: Optional[str] = None,
    include_year_and_category: bool = False
) -> list[dict]:
    formatted = []
    amount_key = f"{year}"
    processing_type = ""


    for row in data:
        cultivate = row["cultivar"]
        amount_str = row.get(amount_key, "-").replace(".", "")
    
        amount = int(amount_str) if amount_str != "-" else 0

        if cultivate.isupper():
            processing_type = cultivate
            continue
        if amount == 0:
            continue

        item = {
            "cultivate": cultivate,
            "amount": amount,
        }
        
        if processing_type:
            item["type"] = processing_type

        if include_year_and_category:
            item["year"] = year
            item["category"] = category

        formatted.append(item)

    return formatted