from fastapi import FastAPI
from app.predict_function import predict
from app.csv_function import get_random_clients
from app.middleware.secure import AuthMiddleware


app = FastAPI(title="Service API")

app.add_middleware(AuthMiddleware)

@app.post("/clients/{client_id}/insights")
async def prediction(client_id: int):
    return predict(client_id)

@app.post("/random-cli")
async def random_clients():
    return get_random_clients()

@app.get("/health")
def health():
    return {"status": "ok"}
