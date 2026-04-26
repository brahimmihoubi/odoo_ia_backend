from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


class CustomerCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None


@router.get("/")
def get_customers(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    customers = models.execute_kw(
        ODOO_DB, uid, password,
        "res.partner", "search_read",
        [[("customer_rank", ">", 0)]],
        {"fields": ["id", "name", "email", "phone"], "limit": 10}
    )

    return {"customers": customers}


@router.post("/")
def create_customer(req: CustomerCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    new_id = models.execute_kw(
        ODOO_DB, uid, password,
        "res.partner", "create",
        [{
            "name": req.name,
            "email": req.email,
            "phone": req.phone,
            "customer_rank": 1
        }]
    )

    return {"status": "success", "id": new_id}