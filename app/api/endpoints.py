from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from app.core.constants import EXPORT_CATEGORY_MAP, END_EXPORT_YEAR, START_EXPORT_YEAR
from app.core.utils import validate_category, validate_year
from app.scraping.export import format_import_data, get_import_data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/export/{category}/{year}", summary="Exportar dados por categoria e ano")
async def get_import_data_by_category_year(category: str, year: int):
    """
    Retorna os dados de exportação para uma categoria e ano específicos.

    Passos realizados:
      1. Valida se a categoria informada está entre as categorias permitidas: 'vinhos, espumantes, uvas_frescas e suco_uva'.
      2. Valida se o ano está dentro do intervalo permitido entre 1970 a 2024.
      3. Chama a função `get_import_data` para obter os dados de exportação do site ou do CSV em caso de erro.
      4. Formata os dados utilizando a função `format_import_data`.
      5. Retorna os dados formatados, ou um status HTTP apropriado caso nenhum dado seja encontrado.

    Parâmetros:
      - category (str): Categoria dos dados de exportação. Deve ser uma das categorias definidas em EXPORT_CATEGORY_MAP.
      - year (int): Ano para o qual os dados de exportação são requisitados. Deve estar entre START_EXPORT_YEAR e END_EXPORT_YEAR.

    Respostas:
      - 200: Dados de exportação retornados e formatados com sucesso.
      - 204: Nenhum dado de exportação disponível para a categoria e ano informados.
      - 400: Categoria ou ano inválido.
      - 500: Falha ao recuperar os dados de exportação.
    """
    allowed_categories = list(EXPORT_CATEGORY_MAP)

    try:
        validate_category(category, allowed_categories)
        validate_year(year, START_EXPORT_YEAR, END_EXPORT_YEAR)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = get_import_data(category, year)
    if data is None:
        raise HTTPException(status_code=500, detail="Falha ao recuperar os dados de exportação.")

    formatted = format_import_data(data, year)

    if not formatted:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    return formatted


@router.get("/export/all", summary="Exportar dados de todas as categorias e anos")
async def get_all_import_data():
    """
    Retorna os dados de exportação para todas as categorias e anos disponíveis.

    Passos realizados:
      1. Itera sobre cada categoria definida em EXPORT_CATEGORY_MAP:'vinhos, espumantes, uvas_frescas e suco_uva'.
      2. Para cada categoria, itera sobre os anos entre 1970 a 2024.
      3. Obtém os dados através da função `get_import_data`.
      4. Formata os dados utilizando a função `format_import_data`, incluindo as informações de categoria e ano.
      5. Agrega todos os registros formatados e os retorna.

    Respostas:
      - 200: Todos os dados de exportação agregados foram retornados com sucesso.
      - 204: Nenhum dado de exportação disponível para as combinações de categoria e ano.
      
    Observação:
      Se ocorrer um erro na obtenção ou formatação dos dados para alguma combinação específica,
      o erro será registrado e o processamento continuará para as demais combinações.
    """
    allowed_categories = list(EXPORT_CATEGORY_MAP)
    all_data = []

    for category in allowed_categories:
        for year in range(START_EXPORT_YEAR, END_EXPORT_YEAR + 1):
            try:
                data = get_import_data(category, year)
                if data is None:
                    logger.warning(f"Dados não encontrados para a categoria '{category}' e ano '{year}'.")
                    continue

                formatted = format_import_data(
                    data,
                    year,
                    category=EXPORT_CATEGORY_MAP[category]["name"],
                    include_year_and_category=True
                )
                all_data.extend(formatted)
            except Exception as e:
                logger.warning(f"Erro ao processar a categoria '{category}', ano '{year}': {e}")
                continue

    if not all_data:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    return all_data