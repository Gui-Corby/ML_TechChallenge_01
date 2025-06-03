from app.core.constants import PRODUCTION_BASE_URL, PRODUCTION_CSV_PATH, PRODUCTION_CSV_COLUMNS
from app.core.utils import load_from_csv, scrape_table_data_from_site


def get_production_data(year: int) -> list[dict]:
    url = PRODUCTION_BASE_URL.format(year=year)

    try:
        return scrape_table_data_from_site(
            url,
            year,
            parse_row_fn=parse_production_row,
            expected_col_range=(2, 2)
        )
    except Exception:
        return load_from_csv(PRODUCTION_CSV_PATH, year, PRODUCTION_CSV_COLUMNS)


def parse_production_row(columns, year: int) -> dict:
    product = columns[0].get_text(strip=True)
    amount = columns[1].get_text(strip=True)

    return {
        "produto": product,
        f"{year}": amount
    }


def format_production_data(
    data: list[dict],
    year: int,
    include_year: bool = False
) -> list[dict]:
    formatted = []
    amount_key = f"{year}"
    product_type = ""

    for row in data:
        product = row["produto"]
        amount_str = row.get(amount_key, "-").replace(".", "")
        amount = int(amount_str) if amount_str != "-" else 0

        if product.isupper():
            product_type = product
            continue
        if amount == 0:
            continue

        item = {
            "product": product,
            "amount": amount,
        }

        if product_type:
            item["type"] = product_type

        if include_year:
            item["year"] = year

        formatted.append(item)

    return formatted