from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


class PurchaseCreate(BaseModel):
    partner_id: int


@router.get("/")
def get_purchases(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    purchases = models.execute_kw(
        ODOO_DB, uid, password,
        "purchase.order", "search_read",
        [[]],
        {"fields": ["id", "name", "amount_total"], "limit": 10}
    )

    return {"purchases": purchases}


@router.post("/")
def create_purchase(req: PurchaseCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    new_id = models.execute_kw(
        ODOO_DB, uid, password,
        "purchase.order", "create",
        [{"partner_id": req.partner_id}]
    )

    return {"status": "success", "id": new_id}