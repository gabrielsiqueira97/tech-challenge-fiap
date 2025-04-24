from fastapi import FastAPI
from app.routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    """Endpoint inicial para testar se a API está rodando"""
    return {"mensagem": "API FastAPI está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)