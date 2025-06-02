from typing import Optional
from bs4 import BeautifulSoup
import requests
from app.core.constants import COMMERCIALIZATION_BASE_URL, COMMERCIALIZATION_CSV_PATH, COMMERCIALIZATION_CSV_COLUMNS
from app.core.utils import load_from_csv


def get_commercialization_data(year: int) -> list[dict]:
    url = COMMERCIALIZATION_BASE_URL.format(year=year)
   
    try:
        return scrape_commercialization_data_from_site(url, year)
    except Exception:
        return load_from_csv(COMMERCIALIZATION_CSV_PATH, year, COMMERCIALIZATION_CSV_COLUMNS)


def scrape_commercialization_data_from_site(url: str, year: int) -> list[dict]:

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
        if len(columns) != 2:
            continue

        product = columns[0].get_text(strip=True)
        amount_raw = columns[1].get_text(strip=True)
        

        data.append({
            "produto": product,
            f"{year}": amount_raw,
        })

    return data

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
