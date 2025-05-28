from bs4 import BeautifulSoup
import requests
import time
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.core.constants import COMMERCIALIZATION_BASE_URL, COMMERCIALIZATION_CSV_COLUMNS
from ..core.utils import load_from_csv


def get_commercialization_data(year: int) -> list[dict]:

    url = COMMERCIALIZATION_BASE_URL.format(year=year)

    try:
        return scrape_commercialization_of_the_year(url, year)
    except Exception:
        return load_from_csv(
            "comercializacao.csv", year, COMMERCIALIZATION_CSV_COLUMNS
        )

def scrape_commercialization_of_the_year(url: str, year: int) -> dict:
    """Retorna a comercialização de vinho do ano

    Args:
        url (str): Link do site
        year (int): Ano
    Returns:
        dict: Dicionário contendo os tipos de vinho e quantidade comercializada no ano
    """
    all_commercialization_data = []

    max_attempts = 20
    attempt = 0

    while attempt < max_attempts:
        try:
            page = requests.get(url, timeout=10)
            page.raise_for_status()  # raise an error for bad responses
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
    
    soup = BeautifulSoup(page.text, "html.parser")
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
            all_commercialization_data.append(data_dict)

    for dict in all_commercialization_data:
        del dict['ano']
        if dict['categoria'] == dict['bebida']:
            del dict['bebida']
            dict['quantidadeLTotal'] = dict['quantidadeL']
            del dict['quantidadeL']
    all_commercialization_data.pop(-1)

    print(f"Year {year} scraped successfully.")

    return {
        "drinks": all_commercialization_data,
        "total_ano": year_total
    }
