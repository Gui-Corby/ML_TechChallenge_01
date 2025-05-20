from bs4 import BeautifulSoup
import requests
from app.core.constants import IMPORT_BASE_URL, IMPORT_CATEGORY_MAP, IMPORT_CSV_COLUMNS
from app.core.utils import load_from_csv


def get_import_data(category: str, year: int):
    config = IMPORT_CATEGORY_MAP.get(category)

    url = IMPORT_BASE_URL.format(year=year, suboption=config["suboption"])

    try:
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
            kg_raw = columns[1].get_text(strip=True)
            value_raw = columns[2].get_text(strip=True)

            data.append({
                "País": country,
                f"{year}_1": kg_raw,
                f"{year}_2": value_raw
            })

        return format_import_data(data)
    
    except Exception as e:
        data = load_from_csv(config["data_path"], year, IMPORT_CSV_COLUMNS)
        return format_import_data(data)
    

def format_import_data(data):
    formatted = []
    for row in data:
        country = row["País"]
        amount_str = row.get("1970_1", "-").replace(".", "")
        value_str = row.get("1970_2", "-").replace(".", "")

        amount = int(amount_str) if amount_str != "-" else 0
        value = int(value_str) if value_str != "-" else 0

        if amount == 0 and value == 0:
            continue

        formatted.append({
            "País": country,
            "Quantidade (Kg)": amount,
            "Valor (US$)": value
        })

    return formatted

