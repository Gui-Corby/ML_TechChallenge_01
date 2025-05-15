import os
import time
from bs4 import BeautifulSoup
import requests
import json

YEAR = 1970


def scrape_production_data():
    all_production_data = []

    # Loop through the years from 1970 to 2024
    for year in range(YEAR, 2024):
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
        # Persist until the year is successfully retrieved.
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
            continue  # try again for this year
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
        print(f"Year {year} scraped successfully.")

    # Saving all the accumulated data to one JSON file
    if os.path.exists("productions.json"):
        with open("productions.json", "r") as file:
            existing_data = json.load(file)
    else:
        # If the file doesn't exist, create an empty list
        existing_data = []
    updated_data = existing_data + all_production_data

    # Writes the updated data to the JSON file
    with open("productions.json", "w") as file:
        json.dump(updated_data, file, indent=4)


scrape_production_data()
