from fastapi import Header, HTTPException
from services.auth import verify_token
from services.session import get_session
from services.odoo import get_odoo_connection


def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Invalid token format")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")

    session = get_session(username)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired")

    password = session["password"]

    uid, models = get_odoo_connection(username, password)
    if not uid:
        raise HTTPException(status_code=401, detail="Odoo auth failed")

    return {
        "uid": uid,
        "models": models,
        "password": password
    }