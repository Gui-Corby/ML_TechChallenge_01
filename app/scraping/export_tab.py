from typing import Optional
from app.core.constants import EXPORT_BASE_URL, EXPORT_CATEGORY_MAP, EXPORT_CSV_COLUMNS
from app.core.utils import load_from_csv, scrape_table_data_from_site


def get_export_data(category: str, year: int) -> list[dict]:
    config = EXPORT_CATEGORY_MAP.get(category)
    url = EXPORT_BASE_URL.format(year=year, suboption=config["suboption"])

    try:
        return scrape_table_data_from_site(
            url,
            year,
            parse_row_fn=parse_export_row,
            expected_col_range=(3, 3)
        )
    except Exception:
        return load_from_csv(config["data_path"], year, EXPORT_CSV_COLUMNS)

def parse_export_row(columns, year: int) -> dict:
    country = columns[0].get_text(strip=True)
    amount = columns[1].get_text(strip=True)
    value = columns[2].get_text(strip=True)

    return {
        "País": country,
        f"{year}_1": amount,
        f"{year}_2": value
    }

def format_export_data(
    data: list[dict],
    year: int,
    category: Optional[str] = None,
    include_year_and_category: bool = False
) -> list[dict]:
    formatted = []
    amount_key = f"{year}_1"
    value_key = f"{year}_2"

    for row in data:
        country = row["País"]
        amount_str = row.get(amount_key, "-").replace(".", "")
        value_str = row.get(value_key, "-").replace(".", "")

        amount = int(amount_str) if amount_str != "-" else 0
        value = int(value_str) if value_str != "-" else 0

        if amount == 0 and value == 0:
            continue

        item = {
            "country": country,
            "amount": amount,
            "value": value
        }

        if include_year_and_category:
            item["year"] = year
            item["category"] = category

        formatted.append(item)

    return formatted
