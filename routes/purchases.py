from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


class PurchaseOrderLineCreate(BaseModel):
    product_id: int
    product_qty: float = 1.0
    price_unit: float = 0.0


class PurchaseCreate(BaseModel):
    partner_id: int
    date_order: Optional[str] = None
    notes: Optional[str] = None
    order_lines: Optional[List[PurchaseOrderLineCreate]] = []


@router.get("/")
def get_purchases(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    state: Optional[str] = Query(None, description="Filter by state: draft, sent, purchase, done, cancel"),
    user=Depends(get_current_user),
):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    domain = []
    if state:
        domain.append(("state", "=", state))

    purchases = models.execute_kw(
        ODOO_DB, uid, password,
        "purchase.order", "search_read",
        [domain],
        {
            "fields": [
                "id", "name", "partner_id", "state",
                "amount_untaxed", "amount_tax", "amount_total",
                "currency_id", "user_id",
                "date_order", "date_approve", "date_planned",
                "invoice_status", "create_date",
            ],
            "limit": limit,
            "offset": offset,
            "order": "date_order desc",
        },
    )

    total = models.execute_kw(
        ODOO_DB, uid, password, "purchase.order", "search_count", [domain]
    )

    return {"purchases": purchases, "total": total}


@router.get("/{order_id}/lines")
def get_purchase_lines(order_id: int, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    lines = models.execute_kw(
        ODOO_DB, uid, password,
        "purchase.order.line", "search_read",
        [[("order_id", "=", order_id)]],
        {
            "fields": [
                "id", "product_id", "name", "product_qty",
                "price_unit", "price_subtotal", "price_total",
                "qty_received", "qty_invoiced", "state",
            ]
        },
    )
    return {"lines": lines}


@router.post("/")
def create_purchase(req: PurchaseCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    vals = {"partner_id": req.partner_id}
    if req.date_order:
        vals["date_order"] = req.date_order
    if req.notes:
        vals["notes"] = req.notes

    if req.order_lines:
        vals["order_line"] = [
            (0, 0, {
                "product_id": line.product_id,
                "product_qty": line.product_qty,
                "price_unit": line.price_unit,
            })
            for line in req.order_lines
        ]

    new_id = models.execute_kw(
        ODOO_DB, uid, password, "purchase.order", "create", [vals]
    )
    return {"status": "success", "id": new_id}

@router.put("/{order_id}")
def update_purchase_order(order_id: int, req: dict, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "purchase.order", "write", [[order_id], req])
    return {"status": "success", "id": order_id}

@router.delete("/{order_id}")
def delete_purchase_order(order_id: int, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "purchase.order", "unlink", [[order_id]])
    return {"status": "success"}
