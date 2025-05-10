from bs4 import BeautifulSoup
import requests

ANO = 1970

url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ANO}&opcao=opt_02"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("tbody")
data = table.find_all("tr")

for row in data:
    columns = row.find_all("td")
    if len(columns) >= 2:
        drink = columns[0].text.strip()
        quantity = columns[1].text.strip()
        print(f"{drink}: {quantity}")
