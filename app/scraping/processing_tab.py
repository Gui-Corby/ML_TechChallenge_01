from typing import Optional
from bs4 import BeautifulSoup
import requests
from app.core.constants import PROCESSING_BASE_URL, PROCESSING_CATEGORY_MAP, PROCESSING_CSV_COLUMNS
from app.core.utils import load_from_csv


def get_processing_data(category: str, year: int) -> list[dict]:
    config = PROCESSING_CATEGORY_MAP.get(category)
    url = PROCESSING_BASE_URL.format(year=year, suboption=config["suboption"])

    try:
       return scrape_processing_data_from_site(url, year)
    except Exception:
        return load_from_csv(config["data_path"], year, PROCESSING_CSV_COLUMNS)

def scrape_processing_data_from_site(url: str, year: int) -> list[dict]:

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

        cultive = columns[0].get_text(strip=True)
        amount_raw = columns[1].get_text(strip=True)
        

        data.append({
            "Cultivar": cultive,
            f"{year}": amount_raw,
            
        })

    return data

def format_processing_data(
    data: list[dict],
    year: int,
    category: Optional[str] = None,
    include_year_and_category: bool = False
) -> list[dict]:
    formatted = []
    amount_key = f"{year}"


    for row in data:
        cultive = row["cultivar"]
        amount_str = row.get(amount_key, "-").replace(".", "")
    
        amount = int(amount_str) if amount_str != "-" else 0
    

        if amount == 0:
            continue

        item = {
            "Cultivar": cultive,
            "Quantidade (Kg)": amount
        }

        if include_year_and_category:
            item["Ano"] = year
            item["Categoria"] = category

        formatted.append(item)

    return formatted