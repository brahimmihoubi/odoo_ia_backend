from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.odoo import get_odoo_connection
from services.auth import create_access_token
from services.session import create_session

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(req: LoginRequest):
    uid, _ = get_odoo_connection(req.username, req.password)

    if not uid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    create_session(req.username, req.password, uid)

    token = create_access_token(req.username, uid)

    return {
        "access_token": token,
        "token_type": "bearer"
    }