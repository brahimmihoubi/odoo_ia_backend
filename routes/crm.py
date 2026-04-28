from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Optional
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


class LeadCreate(BaseModel):
    name: str
    expected_revenue: float
    partner_id: int
    stage_id: Optional[int] = None
    priority: Optional[str] = "0"
    description: Optional[str] = None


@router.get("/")
def get_crm(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user=Depends(get_current_user),
):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    leads = models.execute_kw(
        ODOO_DB, uid, password,
        "crm.lead", "search_read",
        [[]],
        {
            "fields": [
                "id", "name", "partner_id", "stage_id",
                "expected_revenue", "probability", "priority",
                "user_id", "team_id", "date_deadline",
                "create_date", "write_date", "active",
                "email_from", "phone", "type"
            ],
            "limit": limit,
            "offset": offset,
            "order": "create_date desc",
        },
    )

    total = models.execute_kw(
        ODOO_DB, uid, password, "crm.lead", "search_count", [[]]
    )

    return {"leads": leads, "total": total}


@router.get("/stages")
def get_crm_stages(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    stages = models.execute_kw(
        ODOO_DB, uid, password,
        "crm.stage", "search_read",
        [[]],
        {"fields": ["id", "name", "sequence", "probability"], "order": "sequence asc"},
    )
    return {"stages": stages}


@router.post("/")
def create_lead(req: LeadCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    vals = {
        "name": req.name,
        "expected_revenue": req.expected_revenue,
        "partner_id": req.partner_id,
        "type": "opportunity",
        "priority": req.priority,
    }
    if req.stage_id:
        vals["stage_id"] = req.stage_id
    if req.description:
        vals["description"] = req.description

    new_id = models.execute_kw(
        ODOO_DB, uid, password, "crm.lead", "create", [vals]
    )
    return {"status": "success", "id": new_id}

@router.put("/{lead_id}")
def update_crm_lead(lead_id: int, req: dict, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "crm.lead", "write", [[lead_id], req])
    return {"status": "success", "id": lead_id}

@router.delete("/{lead_id}")
def delete_crm_lead(lead_id: int, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "crm.lead", "unlink", [[lead_id]])
    return {"status": "success"}
