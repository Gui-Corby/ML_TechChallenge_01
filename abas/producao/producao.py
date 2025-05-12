from bs4 import BeautifulSoup
import requests
import json

ANO = 1970


def scrape_production_data():
    all_production_data = []
    for year in range(ANO, 2024):
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("tbody")
        data = table.find_all("tr")
    
        for row in data:
            columns = row.find_all("td")
            if len(columns) >= 2:
                drink = columns[0].text.strip()
                quantity = columns[1].text.strip()
                data_dict = {
                    "ano": year,
                    "bebida": drink,
                    "quantidade(L)": quantity
                }
                all_production_data.append(data_dict)

    # Saving all the accumulated data to one JSON file
    with open("productions.json", "w") as file:
        json.dump(all_production_data, file, indent=4)


# Chama a função para fazer o scraping
scrape_production_data()

