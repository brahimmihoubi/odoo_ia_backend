from fastapi import APIRouter, Depends
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


@router.get("/")
def get_companies(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    companies = models.execute_kw(
        ODOO_DB, uid, password,
        "res.company", "search_read",
        [[]],
        {"fields": ["id", "name"], "limit": 10}
    )

    return {"companies": companies}