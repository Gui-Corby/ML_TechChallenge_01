from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI()

# Incluindo as rotas da API
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API is running!"}
