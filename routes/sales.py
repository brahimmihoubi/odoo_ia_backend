from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


class SaleCreate(BaseModel):
    partner_id: int


@router.get("/")
def get_sales(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    sales = models.execute_kw(
        ODOO_DB, uid, password,
        "sale.order", "search_read",
        [[]],
        {"fields": ["id", "name", "amount_total"], "limit": 10}
    )

    return {"sales": sales}


@router.post("/")
def create_sale(req: SaleCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    new_id = models.execute_kw(
        ODOO_DB, uid, password,
        "sale.order", "create",
        [{"partner_id": req.partner_id}]
    )

    return {"status": "success", "id": new_id}