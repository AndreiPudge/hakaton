from fastapi import APIRouter
from backend.app.api.schemas import MLRequest, MLResponse

router = APIRouter()

@router.post("/predict", response_model=MLResponse)
async def predict(request: MLRequest):
    # Заглушка - ML возвращает один float
    fake_prediction = 120000.0
    
    return MLResponse(prediction=fake_prediction)

#@router.get("/test")
#async def buttons_test():
#    return {"message": "Buttons endpoint works!"}