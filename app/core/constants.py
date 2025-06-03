import os 

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

PRODUCTION_START_YEAR = 1970
PRODUCTION_END_YEAR = 2024
PROCESSING_START_YEAR = 1970
PROCESSING_END_YEAR = 2024
COMMERCIALIZATION_START_YEAR = 1970
COMMERCIALIZATION_END_YEAR = 2024
IMPORT_START_YEAR = 1970
IMPORT_END_YEAR = 2024
EXPORT_START_YEAR = 1970
EXPORT_END_YEAR = 2024

PRODUCTION_BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
PROCESSING_BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao={suboption}"
COMMERCIALIZATION_BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_04"
IMPORT_BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao={suboption}"
EXPORT_BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao={suboption}"

PRODUCTION_CSV_COLUMNS = ["produto"]
PROCESSING_CSV_COLUMNS = ["cultivar"]
COMMERCIALIZATION_CSV_COLUMNS = ["produto"]
IMPORT_CSV_COLUMNS = ["País"]
EXPORT_CSV_COLUMNS = ["País"]

PROCESSING_CATEGORY_MAP = {
    "viniferas": {"suboption": "subopt_01", "data_path": "processing_viniferas.csv", "name": "Viniferas"},
    "americanas": {"suboption": "subopt_02", "data_path": "processing_americanas.csv", "name": "Americanas e hibridas"}, 
    "uva_mesa": {"suboption": "subopt_03", "data_path": "processing_uva_mesa.csv", "name": "Uvas de mesa"},
    "sem_class": {"suboption": "subopt_04", "data_path": "processing_sem_class.csv", "name": "Sem classificacao"},
}    
IMPORT_CATEGORY_MAP = {
    "vinhos": {"suboption": "subopt_01", "data_path": "import_vinhos.csv", "name": "Vinhos de mesa"},
    "espumantes": {"suboption": "subopt_02", "data_path": "import_espumantes.csv", "name": "Espumantes"},
    "uvas_frescas": {"suboption": "subopt_03", "data_path": "import_uvas_frescas.csv", "name": "Uvas frescas"},
    "uvas_passas": {"suboption": "subopt_04", "data_path": "import_uvas_passas.csv", "name": "Uvas passas"},
    "suco_uva": {"suboption": "subopt_05", "data_path": "import_suco_uva.csv", "name": "Suco de uva"},
}
EXPORT_CATEGORY_MAP = {
    "vinhos": {"suboption": "subopt_01", "data_path": "export_vinhos.csv", "name": "Vinhos de mesa"},
    "espumantes": {"suboption": "subopt_02", "data_path": "export_espumantes.csv", "name": "Espumantes"},
    "uvas_frescas": {"suboption": "subopt_03", "data_path": "export_uvas_frescas.csv", "name": "Uvas frescas"},
    "suco_uva": {"suboption": "subopt_04", "data_path": "export_suco_uva.csv", "name": "Suco de uva"},
}
PRODUCTION_CSV_PATH = "production.csv"
COMMERCIALIZATION_CSV_PATH = "commercialization.csv"