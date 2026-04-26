from fastapi import APIRouter, Depends
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


@router.get("/")
def dashboard(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    return {
        "sales": models.execute_kw(ODOO_DB, uid, password, "sale.order", "search_count", [[]]),
        "crm": models.execute_kw(ODOO_DB, uid, password, "crm.lead", "search_count", [[]]),
        "customers": models.execute_kw(ODOO_DB, uid, password, "res.partner", "search_count", [[("customer_rank", ">", 0)]])
    }