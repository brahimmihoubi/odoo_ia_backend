from fastapi import APIRouter, Depends
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


@router.get("/")
def get_companies(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    companies = models.execute_kw(
        ODOO_DB, uid, password,
        "res.company", "search_read",
        [[]],
        {
            "fields": [
                "id", "name", "email", "phone",
                "street", "city", "zip", "country_id",
                "vat", "website", "currency_id",
                "logo",
            ],
        },
    )

    return {"companies": companies}

@router.put("/{company_id}")
def update_res_company(company_id: int, req: dict, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "res.company", "write", [[company_id], req])
    return {"status": "success", "id": company_id}

@router.delete("/{company_id}")
def delete_res_company(company_id: int, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    models.execute_kw(ODOO_DB, uid, password, "res.company", "unlink", [[company_id]])
    return {"status": "success"}

from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    country_id: int | None = None
    vat: str | None = None

@router.post("/")
def create_company(req: CompanyCreate, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    vals = {"name": req.name}
    if req.email: vals["email"] = req.email
    if req.phone: vals["phone"] = req.phone
    if req.street: vals["street"] = req.street
    if req.city: vals["city"] = req.city
    if req.country_id: vals["country_id"] = req.country_id
    if req.vat: vals["vat"] = req.vat

    new_id = models.execute_kw(ODOO_DB, uid, password, "res.company", "create", [vals])
    return {"status": "success", "id": new_id}
