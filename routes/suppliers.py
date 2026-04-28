from fastapi import APIRouter, Depends, Query
from typing import Optional
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


@router.get("/")
def get_suppliers(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    user=Depends(get_current_user),
):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    domain = [("supplier_rank", ">", 0)]
    if search:
        domain += [("name", "ilike", search)]

    suppliers = models.execute_kw(
        ODOO_DB, uid, password,
        "res.partner", "search_read",
        [domain],
        {
            "fields": [
                "id", "name", "email", "phone", "mobile",
                "street", "city", "zip", "country_id",
                "supplier_rank", "customer_rank",
                "vat", "website", "active",
                "purchase_order_count", "create_date",
            ],
            "limit": limit,
            "offset": offset,
            "order": "name asc",
        },
    )

    total = models.execute_kw(
        ODOO_DB, uid, password, "res.partner", "search_count", [domain]
    )

    return {"suppliers": suppliers, "total": total}

@router.put("/{supplier_id}")
def update_res_partner(supplier_id: int, req: dict, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "res.partner", "write", [[supplier_id], req])
    return {"status": "success", "id": supplier_id}

@router.delete("/{supplier_id}")
def delete_res_partner(supplier_id: int, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "res.partner", "unlink", [[supplier_id]])
    return {"status": "success"}

from pydantic import BaseModel

class SupplierCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    country_id: int | None = None
    vat: str | None = None

@router.post("/")
def create_supplier(req: SupplierCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    vals = {
        "name": req.name,
        "supplier_rank": 1,
    }
    if req.email: vals["email"] = req.email
    if req.phone: vals["phone"] = req.phone
    if req.street: vals["street"] = req.street
    if req.city: vals["city"] = req.city
    if req.country_id: vals["country_id"] = req.country_id
    if req.vat: vals["vat"] = req.vat

    new_id = models.execute_kw(ODOO_DB, uid, password, "res.partner", "create", [vals])
    return {"status": "success", "id": new_id}
