from bs4 import BeautifulSoup
from typing import List
import requests
import json


def generate_url(tab: str, year: int) -> str:
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={tab}"
    return url


def get_page(url: str) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup


def commercialization_of_the_year(tab: str, year: int) -> List[str]:
    """Retorna a comercialização de vinho do ano

    Args:
        tab (str): Tipo da aba
        year (int): Ano
    Returns:
        List[str]: Lista contendo os tipos de vinho e quantidade comercializada no ano
    """
    all_commercialization_data = []
    url = generate_url(tab, year)
    page = get_page(url)
    table = page.find("tbody")
    data = table.find_all("tr")
    for row in data:
        columns = row.find_all("td")
        if len(columns) >= 2:
            drink = columns[0].text.strip()
            quantity = columns[1].text.strip()
            data_dict = {"ano": year, "bebida": drink, "quantidade(L)": quantity}
            all_commercialization_data.append(data_dict)
    #print(all_commercialization_data)
    return all_commercialization_data

def scrape_commercialization_data(tab, ano="1970"):

    all_commercialization_data = []

    for year in range(ano, 2024):
        all_commercialization_data.append(commercialization_of_the_year(tab, year))

    print(all_commercialization_data)

# Chama a função para fazer o scraping
# scrape_commercialization_data()
#commercialization_of_the_year("opt_04", 2023)
scrape_commercialization_data("opt_04", 2023)
