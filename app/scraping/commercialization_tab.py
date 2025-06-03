from app.core.constants import COMMERCIALIZATION_BASE_URL, COMMERCIALIZATION_CSV_PATH, COMMERCIALIZATION_CSV_COLUMNS
from app.core.utils import load_from_csv, scrape_table_data_from_site


def get_commercialization_data(year: int) -> list[dict]:
    url = COMMERCIALIZATION_BASE_URL.format(year=year)

    try:
        return scrape_table_data_from_site(
            url,
            year,
            parse_row_fn=parse_commercialization_row,
            expected_col_range=(2, 2)
        )
    except Exception:
        return load_from_csv(COMMERCIALIZATION_CSV_PATH, year, COMMERCIALIZATION_CSV_COLUMNS)

def parse_commercialization_row(columns, year: int) -> dict:
    product = columns[0].get_text(strip=True)
    amount = columns[1].get_text(strip=True)

    return {
        "produto": product,
        f"{year}": amount
    }

def format_commercialization_data(
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
