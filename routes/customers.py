from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Optional
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


class CustomerCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    vat: Optional[str] = None


@router.get("/")
def get_customers(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    user=Depends(get_current_user),
):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    domain = [("customer_rank", ">", 0)]
    if search:
        domain += [("name", "ilike", search)]

    customers = models.execute_kw(
        ODOO_DB, uid, password,
        "res.partner", "search_read",
        [domain],
        {
            "fields": [
                "id", "name", "email", "phone", "mobile",
                "street", "city", "zip", "country_id",
                "customer_rank", "supplier_rank",
                "vat", "website", "active",
                "sale_order_count", "purchase_order_count",
                "create_date",
            ],
            "limit": limit,
            "offset": offset,
            "order": "name asc",
        },
    )

    total = models.execute_kw(
        ODOO_DB, uid, password, "res.partner", "search_count", [domain]
    )

    return {"customers": customers, "total": total}


@router.get("/{customer_id}")
def get_customer(customer_id: int, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    result = models.execute_kw(
        ODOO_DB, uid, password,
        "res.partner", "read",
        [[customer_id]],
        {"fields": [
            "id", "name", "email", "phone", "mobile",
            "street", "city", "zip", "country_id",
            "customer_rank", "supplier_rank",
            "vat", "website", "active",
            "sale_order_count", "purchase_order_count",
            "create_date", "comment",
        ]},
    )
    return {"customer": result[0] if result else None}


@router.post("/")
def create_customer(req: CustomerCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    vals = {
        "name": req.name,
        "customer_rank": 1,
    }
    if req.email:
        vals["email"] = req.email
    if req.phone:
        vals["phone"] = req.phone
    if req.street:
        vals["street"] = req.street
    if req.city:
        vals["city"] = req.city
    if req.country_id:
        vals["country_id"] = req.country_id
    if req.vat:
        vals["vat"] = req.vat

    new_id = models.execute_kw(
        ODOO_DB, uid, password, "res.partner", "create", [vals]
    )
    return {"status": "success", "id": new_id}

@router.put("/{customer_id}")
def update_res_partner(customer_id: int, req: dict, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "res.partner", "write", [[customer_id], req])
    return {"status": "success", "id": customer_id}

@router.delete("/{customer_id}")
def delete_res_partner(customer_id: int, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "res.partner", "unlink", [[customer_id]])
    return {"status": "success"}
