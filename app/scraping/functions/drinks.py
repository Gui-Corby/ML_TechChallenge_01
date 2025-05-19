from bs4 import BeautifulSoup
import requests
import time
from fastapi.responses import JSONResponse
from app.scraping.production import URL_TEMPLATE


def drinks_scraping(url: str, year: int) -> list:
    url = URL_TEMPLATE.format(year=year)
    all_production_data = []

    while True:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # raise an error for bad responses
            break
        except requests.RequestException as e:
            print(
                f"Error accessing {url} for year {year}: {e}. "
                "Retrying in 5 seconds..."
            )
            time.sleep(5)

    # Start scraping the page
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("tbody")
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
                "quantidade(L)": quantity
            }
            all_production_data.append(data_dict)

    # removing redundant data
    for dict in all_production_data:
        del dict['ano']
        if dict['categoria'] == dict['bebida']:
            del dict['bebida']
            dict['quantidade(L) total'] = dict['quantidade(L)']
            del dict['quantidade(L)']
    print(f"Year {year} scraped successfully.")

    return all_production_data
