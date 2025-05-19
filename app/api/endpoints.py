from fastapi import APIRouter, HTTPException
from bs4 import BeautifulSoup
import requests
import time
from fastapi.responses import JSONResponse
import json
from pathlib import Path
import tracemalloc
import asyncio
import csv
tracemalloc.start()

router = APIRouter()

YEAR = 1970

with open("/Users/gui/Desktop/TechChallenge_01/app/scraping/csv/producao.csv", 'r') as file:
    drinks = []
    csvreader = csv.DictReader(file, delimiter=";")
    header = csvreader.fieldnames
    # print(header)

    if str(YEAR) in header:
        for row in csvreader:
            produto = row['produto'].strip()
            if produto.isupper():
                current_category = produto
                # continue
            drink_data = {
                "categoria": current_category,
                "bebida": row['produto'],
                "quantidade(L)": row[str(YEAR)]
            }
            drinks.append(drink_data)

        for drink in drinks:
            if drink['categoria'] == drink['bebida']:
                del drink['bebida']
                drink['quantidade(L) total'] = drink['quantidade(L)']
                del drink['quantidade(L)']
        print(json.dumps(drinks, indent=4, ensure_ascii=False))

                
            # if row[YEAR]:
            #     production_data = {
            #         "bebida": row['produto'],
            #         "quantidade(L)": row[YEAR]
            #     }
            #     print(production_data)

    # for row in csvreader:
    #     # if row[0] == str(YEAR):
    #     #     production_data = {
    #     #         "ano": row[{YEAR}],
    #     #         "categoria": row['control'],
    #     #         "bebida": row['produto'],
    #     #         # "quantidade(L)": row[3]
    #     #     }
    #         # print(production_data)
    #         print(row)


@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}


# Endpoint to get production data for a specific year.
@router.get("/production/{year}")
async def get_production_data(year: int):
    all_production_data = []

    # Loop through the years from 1970 to 2024

    url = (
        f"http://vitibrasil.cnpuv.embrapa.br/index.php"
        f"?ano={year}&opcao=opt_02"
    )
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
        # try again for this year
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

    for dict in all_production_data:
        del dict['ano']
        if dict['categoria'] == dict['bebida']:
            del dict['bebida']
            dict['quantidade(L) total'] = dict['quantidade(L)']
            del dict['quantidade(L)']
    print(f"Year {year} scraped successfully.")

    print(json.dumps(all_production_data, indent=4,
                     ensure_ascii=False))

    # return all_production_data
# asyncio.run(get_production_data(1970))
