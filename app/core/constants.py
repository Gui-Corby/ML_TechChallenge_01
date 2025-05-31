import os 

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

PRODUCTION_START_YEAR = 1970
PRODUCTION_END_YEAR = 2024
START_PROCESSING_YEAR = 1970
END_PROCESSING_YEAR = 2024
COMMERCIALIZATION_START_YEAR = 1970
COMMERCIALIZATION_END_YEAR = 2024
START_IMPORT_YEAR = 1970
END_IMPORT_YEAR = 2024
START_EXPORT_YEAR = 1970
END_EXPORT_YEAR = 2024

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
    "ProcessaViniferas": {"suboption": "subopt_01", "data_path": "ProcessaViniferas.csv", "name": "Viniferas"},
    "ProcessaAmericanas": {"suboption": "subopt_02", "data_path": "ProcessaAmericanas.csv", "name": "Americanas e hibridas"}, 
    "ProcessaMesa": {"suboption": "subopt_03", "data_path": "ProcessaMesa.csv", "name": "Uvas de mesa"},
    "ProcessaSemclass": {"suboption": "subopt_04", "data_path": "ProcessaSemclass.csv", "name": "Sem classificacao"},
    
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