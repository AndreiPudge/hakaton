from fastapi import APIRouter
from backend.app.api.schemas import ButtonAction

router = APIRouter()

@router.post("/click")
async def handle_button_click(action: ButtonAction):
    # Обработка разных кнопок
    if action.button_id == "":
        return {"message": "", "button": action.button_id}
    elif action.button_id == "":
        return {"message": "", "button": action.button_id}
    elif action.button_id == "":
        return {"message": "", "button": action.button_id}
    else:
        return {"message": f"Button {action.button_id} clicked", "action": action.action}

#@router.get("/test")
#async def buttons_test():
#    return {"message": "Buttons endpoint works!"}