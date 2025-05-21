import os 

IMPORT_CATEGORY_MAP = {
    "vinhos": {"suboption": "subopt_01", "data_path": "import_vinhos.csv", "name": "Vinhos de mesa"},
    "espumantes": {"suboption": "subopt_02", "data_path": "import_espumantes.csv", "name": "Espumantes"},
    "uvas_frescas": {"suboption": "subopt_03", "data_path": "import_uvas_frescas.csv", "name": "Uvas frescas"},
    "uvas_passas": {"suboption": "subopt_04", "data_path": "import_uvas_passas.csv", "name": "Uvas passas"},
    "suco_uva": {"suboption": "subopt_05", "data_path": "import_suco_uva.csv", "name": "Suco de uva"},
}

START_IMPORT_YEAR = 1970
END_IMPORT_YEAR = 2024

IMPORT_BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao={suboption}"
IMPORT_CSV_COLUMNS = ["País"]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")