from fastapi import APIRouter, Depends
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


@router.get("/")
def get_invoices(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    invoices = models.execute_kw(
        ODOO_DB, uid, password,
        "account.move", "search_read",
        [[("move_type", "=", "out_invoice")]],
        {"fields": ["id", "name", "amount_total"], "limit": 10}
    )

    return {"invoices": invoices}