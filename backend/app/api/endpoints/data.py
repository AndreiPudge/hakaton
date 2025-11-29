from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import UserData
from backend.app.api.schemas import UserDataResponse

router = APIRouter()

# GET /api/data/users - получить все данные из БД
@router.get("/users", response_model=list[UserDataResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(UserData).all()
    return users

# GET /api/data/stats - простая статистика
@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    count = db.query(UserData).count()
    avg_value = db.query(UserData.value).scalar() or 0
    return {"total_records": count, "average_value": avg_value}

#@router.get("/test")
#async def data_test():
#    return {"message": "Data endpoint works!"}