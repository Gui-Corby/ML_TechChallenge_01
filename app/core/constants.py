import os

START_YEAR = 1970
END_YEAR = 2024

COMMERCIALIZATION_BASE_URL = (
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_04"
)
COMMERCIALIZATION_CSV_COLUMNS = ["produto"]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
