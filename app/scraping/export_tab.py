from typing import Optional
from bs4 import BeautifulSoup
import requests
from app.core.constants import EXPORT_BASE_URL, EXPORT_CATEGORY_MAP, EXPORT_CSV_COLUMNS
from app.core.utils import load_from_csv


def get_export_data(category: str, year: int) -> list[dict]:
    config = EXPORT_CATEGORY_MAP.get(category)
    url = EXPORT_BASE_URL.format(year=year, suboption=config["suboption"])
   
    try:
        return scrape_export_data_from_site(url, year)
    except Exception:
        return load_from_csv(config["data_path"], year, EXPORT_CSV_COLUMNS)

def scrape_export_data_from_site(url: str, year: int) -> list[dict]:

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    data_table = soup.find("table", class_="tb_base tb_dados")
    if not data_table:
        raise ValueError("Data table not found")

    rows = data_table.find("tbody").find_all("tr")
    data = []

    for tr in rows:
        columns = tr.find_all("td")
        if len(columns) != 3:
            continue

        country = columns[0].get_text(strip=True)
        amount_raw = columns[1].get_text(strip=True)
        value_raw = columns[2].get_text(strip=True)

        data.append({
            "País": country,
            f"{year}_1": amount_raw,
            f"{year}_2": value_raw
        })

    return data

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
