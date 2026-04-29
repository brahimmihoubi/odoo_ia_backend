from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Literal
from services.deps import get_current_user
from services.session import get_session, update_session_theme

router = APIRouter()


class ThemePreference(BaseModel):
    theme: Literal["light", "dark"]


@router.get("/preferences")
def get_user_preferences(user=Depends(get_current_user)):
    session = get_session(user["username"])
    theme = session.get("theme", "light") if session else "light"
    return {"theme": theme}


@router.put("/preferences")
def update_user_preferences(pref: ThemePreference, user=Depends(get_current_user)):
    update_session_theme(user["username"], pref.theme)
    return {"theme": pref.theme}