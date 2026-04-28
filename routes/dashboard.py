from fastapi import APIRouter, Depends
from services.odoo import ODOO_DB
from services.deps import get_current_user

router = APIRouter()


@router.get("/")
def dashboard(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]

    def count(model, domain=None):
        return models.execute_kw(
            ODOO_DB, uid, password, model, "search_count", [domain or []]
        )

    def read_first(model, domain, fields, order=None):
        kwargs = {"fields": fields, "limit": 5}
        if order:
            kwargs["order"] = order
        return models.execute_kw(
            ODOO_DB, uid, password, model, "search_read", [domain], kwargs
        )

    # ── Counts ──────────────────────────────────────────────────────────────
    total_customers = count("res.partner", [("customer_rank", ">", 0)])
    total_suppliers = count("res.partner", [("supplier_rank", ">", 0)])
    total_sales = count("sale.order")
    confirmed_sales = count("sale.order", [("state", "in", ["sale", "done"])])
    total_purchases = count("purchase.order")
    confirmed_purchases = count("purchase.order", [("state", "in", ["purchase", "done"])])
    total_leads = count("crm.lead")
    total_invoices = count("account.move", [("move_type", "=", "out_invoice")])
    unpaid_invoices = count("account.move", [
        ("move_type", "=", "out_invoice"),
        ("payment_state", "!=", "paid"),
        ("state", "=", "posted"),
    ])
    total_bills = count("account.move", [("move_type", "=", "in_invoice")])

    # ── Revenue: sum of confirmed sale order totals ──────────────────────────
    sale_records = models.execute_kw(
        ODOO_DB, uid, password,
        "sale.order", "search_read",
        [[("state", "in", ["sale", "done"])]],
        {"fields": ["amount_total"]},
    )
    total_revenue = sum(r["amount_total"] for r in sale_records)

    # ── Total outstanding invoice amount ────────────────────────────────────
    invoice_records = models.execute_kw(
        ODOO_DB, uid, password,
        "account.move", "search_read",
        [[("move_type", "=", "out_invoice"), ("payment_state", "!=", "paid"), ("state", "=", "posted")]],
        {"fields": ["amount_residual"]},
    )
    total_outstanding = sum(r["amount_residual"] for r in invoice_records)

    # ── Recent activity snapshots ────────────────────────────────────────────
    recent_sales = read_first(
        "sale.order", [],
        ["id", "name", "partner_id", "amount_total", "state", "date_order"],
        order="date_order desc",
    )
    recent_invoices = read_first(
        "account.move",
        [("move_type", "=", "out_invoice")],
        ["id", "name", "partner_id", "amount_total", "payment_state", "invoice_date"],
        order="invoice_date desc",
    )
    recent_leads = read_first(
        "crm.lead", [],
        ["id", "name", "partner_id", "expected_revenue", "stage_id", "create_date"],
        order="create_date desc",
    )

    return {
        "kpis": {
            "total_customers": total_customers,
            "total_suppliers": total_suppliers,
            "total_sales": total_sales,
            "confirmed_sales": confirmed_sales,
            "total_purchases": total_purchases,
            "confirmed_purchases": confirmed_purchases,
            "total_leads": total_leads,
            "total_invoices": total_invoices,
            "unpaid_invoices": unpaid_invoices,
            "total_bills": total_bills,
            "total_revenue": total_revenue,
            "total_outstanding": total_outstanding,
        },
        "recent_sales": recent_sales,
        "recent_invoices": recent_invoices,
        "recent_leads": recent_leads,
    }