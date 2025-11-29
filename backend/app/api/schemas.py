from pydantic import BaseModel
from typing import List

# Для ML
class MLRequest(BaseModel):
    input_data: float

class MLResponse(BaseModel):
    prediction: List[float]  # один float вместо списка
    status: str = "success"

# Для БД
class UserDataResponse(BaseModel):
    id: int
    name: str
    value: float
    category: str

# Для кнопок
class ButtonAction(BaseModel):
    button_id: str
    action: str