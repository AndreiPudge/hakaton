from fastapi import FastAPI
from service.app.predict_function import predict
from service.app.csv_function import get_random_clients
from service.app.middleware.secure import AuthMiddleware


app = FastAPI(title="Service API")

app.add_middleware(AuthMiddleware)

@app.post("/predict")
async def prediction():
    return {"predictions": predict()}

@app.post("/random-cli")
async def random_clients():
    return get_random_clients()

@app.get("/health")
def health():
    return {"status": "ok"}
