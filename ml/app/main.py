from fastapi import FastAPI
from app.csv_function import get_random_clients


app = FastAPI(title="Service API")

@app.post("/clients/{client_id}/insights")
async def prediction(client_id: int):
    #return predict(client_id)
    return "adsa"

@app.post("/random-cli")
async def random_clients():
    return get_random_clients()

@app.get("/health")
def health():
    return {"status": "ok"}
