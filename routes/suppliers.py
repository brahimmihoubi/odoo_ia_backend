from fastapi import APIRouter, Depends
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


@router.get("/")
def get_suppliers(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    suppliers = models.execute_kw(
        ODOO_DB, uid, password,
        "res.partner", "search_read",
        [[("supplier_rank", ">", 0)]],
        {"fields": ["id", "name"], "limit": 10}
    )

    return {"suppliers": suppliers}