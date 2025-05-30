from bs4 import BeautifulSoup
import requests
import time
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ..core.constants import PRODUCTION_BASE_URL, PRODUCTION_CSV_COLUMNS
from ..core.utils import load_from_csv


# Will try to scrape or load from csv
def get_production_data(year: int) -> list[dict]:
    url = PRODUCTION_BASE_URL.format(year=year)

    try:
        data = scrape_production_data_from_site(url, year)
        return (True, data)
    except Exception:
        data = load_from_csv(
            "producao.csv", year, PRODUCTION_CSV_COLUMNS
        )
        return (False, data)


def scrape_production_data_from_site(url: str, year: int) -> list[dict]:
    url = PRODUCTION_BASE_URL.format(year=year)
    all_production_data = []

    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # raise an error for bad responses
            break
        except requests.RequestException:
            attempt += 1
            if attempt >= max_attempts:
                raise HTTPException(
                    status_code=500,
                    detail=(
                        f"Failed to access {url} after {max_attempts} attempts"
                    )
                )
            time.sleep(5)

    # Start scraping the page
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        print(
            f"No table found at {url} for year {year}. "
            "Retrying in 5 seconds..."
        )
        time.sleep(5)
        return JSONResponse(
            content={"error": "No table found"},
            status_code=500
        )
    data = table.find_all("tr")
    year_total = (
        table.find("tfoot", class_="tb_total")
        .find_all("td")[1]
        .text.strip()
    )

    # Getting each item in the rows
    for row in data:
        columns = row.find_all("td")
        category = row.find("td", class_="tb_item")

        if category and category.text.strip():
            current_category = category.text.strip()
        if len(columns) >= 2:
            drink = columns[0].text.strip()
            quantity = columns[1].text.strip()
            data_dict = {
                "ano": year,
                "categoria": current_category,
                "bebida": drink,
                "quantidadeL": quantity
            }
            if drink.lower() == "total":
                continue

            all_production_data.append(data_dict)

    # formatting and removing redundant data
    for dict in all_production_data:
        del dict['ano']
        if dict['categoria'] == dict['bebida']:
            del dict['bebida']
            dict['quantidadeLTotal'] = dict['quantidadeL']
            del dict['quantidadeL']
        if dict.get('quantidadeL', None) == '-':
            dict['quantidadeL'] = '0'

    all_production_data.append({
        "total_ano": year_total
    })

    return all_production_data


# formatting data for csv output
def format_production_data(
    data: list[dict],
    year: int
) -> list[dict]:
    year_str = str(year)
    formatted = []
    last_category = None
    year_total = 0

    for item in data:
        product = item.get("bebida", item.get("produto", "")).strip()
        if product.isupper():
            last_category = product

        item = {
            "categoria": last_category,
            "bebida": product,
            "quantidadeL": item.get(year_str, "")
        }

        formatted.append(item)

    for item in formatted:
        if item["categoria"] == item["bebida"]:
            del item["bebida"]
            item["quantidadeLTotal"] = item["quantidadeL"]
            del item["quantidadeL"]
        item.get("quantidadeLTotal", "0")
        year_total += int(item.get("quantidadeLTotal", 0))

    formatted.append({
        "total_ano": str(year_total)
    })

    return formatted
