from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="API Exportações Vitibrasil",
    description="Consulta dados de produção, processamento, comercialização, importação, exportação e publicação durante o período de 1970 a 2024 da Embrapa para Vinho, Uva, Suco e Outros derivados.",
    version="1.0.0"
)

# Incluindo as rotas da API
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "API is running!"}
