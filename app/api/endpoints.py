from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from app.core.constants import COMMERCIALIZATION_START_YEAR, COMMERCIALIZATION_END_YEAR, END_EXPORT_YEAR, END_PROCESSING_YEAR, EXPORT_CATEGORY_MAP, IMPORT_CATEGORY_MAP, END_IMPORT_YEAR, PROCESSING_CATEGORY_MAP, PRODUCTION_END_YEAR, PRODUCTION_START_YEAR, START_EXPORT_YEAR, START_IMPORT_YEAR, START_PROCESSING_YEAR
from app.core.utils import validate_category, validate_year
from app.scraping.commercialization_tab import format_commercialization_data, get_commercialization_data
from app.scraping.export_tab import format_export_data, get_export_data
from app.scraping.import_tab import format_import_data, get_import_data
from app.scraping.processing_tab import format_processing_data, get_processing_data
from app.scraping.production_tab import format_production_data, get_production_data

logger = logging.getLogger(__name__)
router = APIRouter()


# Endpoint to get production data for a specific year.
@router.get("/production/{year}", summary="Import data for a specific year")
async def get_production_data_by_year(
    year: int,
    limit: int | None = None,
    offset: int | None = None
):
    """
    Returns production data for a specific year, optionally paginated.
    """
    try:
        validate_year(year, PRODUCTION_START_YEAR, PRODUCTION_END_YEAR)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    is_scraped, data = get_production_data(year)

    if not data:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve production data"
        )

    if not is_scraped:
        data = format_production_data(data, year)

    if offset:
        data = data[offset:]
    if limit:
        data = data[:limit]

    return data

@router.get("/processing/{category}/{year}", summary="Processing data by category and year")
async def get_processing_data_by_category_year(category: str, year: int):
    """
    Returns processing data for a given category and year.
    """
    allowed_categories = list(PROCESSING_CATEGORY_MAP)

    try:
        validate_category(category, allowed_categories)
        validate_year(year, START_PROCESSING_YEAR, END_PROCESSING_YEAR)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = get_processing_data(category, year)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve processing data.")

    formatted = format_processing_data(data, year)

    if not formatted:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    return formatted


@router.get("/processing/all", summary="Processing data for all categories and years")
async def get_all_processing_data():
    """
    Returns all available processing data across all categories and years.
    """
    allowed_categories = list(PROCESSING_CATEGORY_MAP)
    all_data = []

    for category in allowed_categories:
        for year in range(START_PROCESSING_YEAR, END_PROCESSING_YEAR + 1):
            try:
                data = get_processing_data(category, year)
                if data is None:
                    logger.warning(f"Data not found '{category}', year '{year}': {e}")
                    continue

                formatted = format_processing_data(
                            data,
                            year,
                            category=PROCESSING_CATEGORY_MAP[category]["name"],
                            include_year_and_category=True
                        )
                all_data.extend(formatted)
            except Exception as e:
                logger.warning(f"Error while processing category '{category}', year '{year}': {e}")
                continue

    if not all_data:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    return all_data

@router.get("/commercialization/{year}", summary="Import data for a specific year")
async def get_commercialization_data_by_year(
    year: int,
    limit: int | None = None,
    offset: int | None = None
):
    """
    Returns commercialization data for a specific year.
    """
    try:
        validate_year(year, COMMERCIALIZATION_START_YEAR, COMMERCIALIZATION_END_YEAR - 1)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    is_scraped, data = get_commercialization_data(year)

    if not data:
        raise HTTPException(status_code=500,
                            detail="Failed to retrieve commercialization data")
    
    if not is_scraped:
        data = format_commercialization_data(data, year)
    
    if offset:
        data = data[offset:]
    if limit:
        data = data[:limit]
    
    return data

@router.get("/import/{category}/{year}", summary="Import data by category and year")
async def get_import_data_by_category_year(category: str, year: int):
    """
    Returns import data for a given category and year.
    """
    allowed_categories = list(IMPORT_CATEGORY_MAP)

    try:
        validate_category(category, allowed_categories)
        validate_year(year, START_IMPORT_YEAR, END_IMPORT_YEAR)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = get_import_data(category, year)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve import data.")

    formatted = format_import_data(data, year)

    if not formatted:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    return formatted


@router.get("/import/all", summary="Import data for all categories and years")
async def get_all_import_data():
    """
    Returns all available import data across all categories and years.
    """
    allowed_categories = list(IMPORT_CATEGORY_MAP)
    all_data = []

    for category in allowed_categories:
        for year in range(START_IMPORT_YEAR, END_IMPORT_YEAR + 1):
            try:
                data = get_import_data(category, year)
                if data is None:
                    logger.warning(f"Data not found '{category}', year '{year}': {e}")
                    continue

                formatted = format_import_data(
                            data,
                            year,
                            category=IMPORT_CATEGORY_MAP[category]["name"],
                            include_year_and_category=True
                        )
                all_data.extend(formatted)
            except Exception as e:
                logger.warning(f"Error while processing category '{category}', year '{year}': {e}")
                continue

    if not all_data:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)

    return all_data

@router.get("/export/{category}/{year}", summary="Exportar dados por categoria e ano")
async def get_export_data_by_category_year(category: str, year: int):
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

    data = get_export_data(category, year)
    if data is None:
        raise HTTPException(status_code=500, detail="Falha ao recuperar os dados de exportação.")

    formatted = format_export_data(data, year)

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
                data = get_export_data(category, year)
                if data is None:
                    logger.warning(f"Dados não encontrados para a categoria '{category}' e ano '{year}'.")
                    continue

                formatted = format_export_data(
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