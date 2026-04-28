from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import (
    auth,
    crm,
    customers,
    sales,
    purchases,
    suppliers,
    companies,
    dashboard,
    invoices,
    ai,
    users
)

app = FastAPI(title="Odoo Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(crm.router, prefix="/api/crm")
app.include_router(customers.router, prefix="/api/customers")
app.include_router(sales.router, prefix="/api/sales")
app.include_router(purchases.router, prefix="/api/purchases")
app.include_router(suppliers.router, prefix="/api/suppliers")
app.include_router(companies.router, prefix="/api/companies")
app.include_router(dashboard.router, prefix="/api/dashboard")
app.include_router(invoices.router, prefix="/api/invoices")
app.include_router(ai.router, prefix="/api/ai")
app.include_router(users.router, prefix="/api/user")


@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Healthy"}