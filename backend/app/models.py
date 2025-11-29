from sqlalchemy import Column, Integer, String, Float
from backend.app.database import Base
from backend.app.database import engine

# Минимальная модель для примера
class UserData(Base):
    __tablename__ = "user_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float)
    category = Column(String)

# Создаем таблицы при старте

Base.metadata.create_all(bind=engine)