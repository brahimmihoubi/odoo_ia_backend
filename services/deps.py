from fastapi import Header, HTTPException
from services.auth import verify_token
from services.session import get_session
from services.odoo import get_odoo_connection


def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token format")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")

    session = get_session(username)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired")

    password = session["password"]
    uid = session["uid"]  # reuse uid from session, no re-auth needed

    # models is an XML-RPC proxy, rebuild it per request
    # but skip expensive authenticate() since uid is already known
    _, models = get_odoo_connection(username, password)
    if not models:
        raise HTTPException(status_code=401, detail="Odoo connection failed")

    return {
        "username": username,  # needed so routes can access session
        "uid": uid,
        "models": models,
        "password": password,
    }