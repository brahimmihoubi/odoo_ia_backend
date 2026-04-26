from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


class LeadCreate(BaseModel):
    name: str
    expected_revenue: float
    partner_id: int


@router.get("/")
def get_crm(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    leads = models.execute_kw(
        ODOO_DB, uid, password,
        "crm.lead", "search_read",
        [[]],
        {"fields": ["id", "name", "expected_revenue"], "limit": 10}
    )

    return {"leads": leads}


@router.post("/")
def create_lead(req: LeadCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    new_id = models.execute_kw(
        ODOO_DB, uid, password,
        "crm.lead", "create",
        [{
            "name": req.name,
            "expected_revenue": req.expected_revenue,
            "partner_id": req.partner_id,
            "type": "opportunity"
        }]
    )

    return {"status": "success", "id": new_id}