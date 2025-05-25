import os 

EXPORT_CATEGORY_MAP = {
    "vinhos": {"suboption": "subopt_01", "data_path": "export_vinhos.csv", "name": "Vinhos de mesa"},
    "espumantes": {"suboption": "subopt_02", "data_path": "export_espumantes.csv", "name": "Espumantes"},
    "uvas_frescas": {"suboption": "subopt_03", "data_path": "export_uvas_frescas.csv", "name": "Uvas frescas"},
    "suco_uva": {"suboption": "subopt_04", "data_path": "export_suco_uva.csv", "name": "Suco de uva"},
}

START_EXPORT_YEAR = 1970
END_EXPORT_YEAR = 2024

EXPORT_BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao={suboption}"
EXPORT_CSV_COLUMNS = ["País"]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")