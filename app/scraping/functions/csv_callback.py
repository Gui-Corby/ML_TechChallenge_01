import csv
# from app.scraping.functions import YEAR


def csv_callback(year: int) -> list:
    all_production_data = []
    with open(
        (
            "/Users/gui/Desktop/TechChallenge_01/app/scraping/"
            "csv/producao.csv"
        ),
        'r'
    ) as file:

        csvreader = csv.DictReader(file, delimiter="""")
        header = csvreader.fieldnames

        if str(year) in header:
            for row in csvreader:
                produto = row['produto'].strip()
                if produto.isupper():
                    current_category = produto
                    continue
                data_dict = {
                    "categoria": current_category,
                    "bebida": row['produto'],
                    "quantidade(L)": row[str(year)]
                }
                all_production_data.append(data_dict)
            for dict in all_production_data:
                if dict['categoria'] == dict['bebida']:
                    del dict['bebida']
                    dict['quantidade(L) total'] = dict['quantidade(L)']
                    del dict['quantidade(L)']
            return all_production_data
