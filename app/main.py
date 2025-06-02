from fastapi import FastAPI
from app.api.commercialization_tab_routes import router as commercialization_router
from app.api.export_tab_routes import router as export_router
from app.api.import_tab_routes import router as import_router
from app.api.processing_tab_routes import router as processing_router
from app.api.production_routes import router as production_router

app = FastAPI(
    title="API Exportações Vitibrasil",
    description="Consulta dados de produção, processamento, comercialização, importação, exportação e publicação durante o período de 1970 a 2024 da Embrapa para Vinho, Uva, Suco e Outros derivados.",
    version="1.0.0"
)

app.include_router(commercialization_router, prefix="/commercialization")
app.include_router(export_router, prefix="/export")
app.include_router(import_router, prefix="/import")
app.include_router(processing_router, prefix="/processing")
app.include_router(production_router, prefix="/production")


@app.get("/")
async def root():
    return {"message": "API is running!"}
